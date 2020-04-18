import pytest
import struct
import gzip
from datetime import datetime
from ..protobufs import cortex_pb2
from ..utils import reader
from . import test_utils as tu


def generate_binary_file(path):
	# user
	bin = struct.pack("q", tu._USER_ID)
	bin += struct.pack("i", len(tu._USERNAME))
	bin += struct.pack("10s", bytes(tu._USERNAME, 'utf-8'))
	bin += struct.pack("i", tu._BIRTHDAY)
	bin += struct.pack("c", bytes(tu._GENDER, 'utf-8'))
	# snapshot
	bin += struct.pack("q", tu._DATETIME)
	bin += struct.pack("ddd", 
		tu._TRANSLATION_X, tu._TRANSLATION_Y, tu._TRANSLATION_Z
		)
	bin += struct.pack("dddd", tu._ROTATION_X,
		tu._ROTATION_Y, tu._ROTATION_Z, tu._ROTATION_W
		)
	bin += struct.pack("ii", tu._C_HEIGHT, tu._C_WIDTH)
	bin += tu._C_DATA
	bin += struct.pack("ii", tu._D_HEIGHT, tu._D_WIDTH)
	bin += struct.pack(f"{len(tu._D_DATA)}f", *tu._D_DATA)
	bin += struct.pack("ffff",
		tu._HUNGER, tu._THIRST, tu._EXHAUSTION, tu._HAPPINESS
		)
	with open(path, "wb+") as f:
		f.write(bin)
	print(bin)


gender_dict = {"m": 0, "f": 1, "o": 2}


def generate_protobuf_file(path):
	user = cortex_pb2.User(
		user_id = tu._USER_ID,
		username = tu._USERNAME,
		birthday = tu._BIRTHDAY,
		gender = gender_dict[tu._GENDER]
		).SerializeToString()
	bin = struct.pack(f"i{len(user)}s", len(user), user)
	snap = cortex_pb2.Snapshot(
		datetime = tu._DATETIME,
		pose = cortex_pb2.Pose(
			translation = cortex_pb2.Pose.Translation(
				x = tu._TRANSLATION_X,
				y = tu._TRANSLATION_Y,
				z = tu._TRANSLATION_Z
				),
			rotation = cortex_pb2.Pose.Rotation(
				w = tu._ROTATION_W,
				x = tu._ROTATION_X,
				y = tu._ROTATION_Y,
				z = tu._ROTATION_Z
				)
			),
		color_image = cortex_pb2.ColorImage(
			width = tu._C_WIDTH,
			height = tu._C_HEIGHT,
			data = tu._C_DATA
			),
		depth_image = cortex_pb2.DepthImage(
			width = tu._D_WIDTH,
			height = tu._D_HEIGHT,
			data = tu._D_DATA
			),
		feelings = cortex_pb2.Feelings(
			hunger = tu._HUNGER,
			thirst = tu._THIRST,
			exhaustion = tu._EXHAUSTION,
			happiness = tu._HAPPINESS
			)
		).SerializeToString()
	bin += struct.pack(f"i{len(snap)}s", len(snap), snap)
	with gzip.open(path, "wb+") as f:
		f.write(bin)


@pytest.fixture(params=[
	(generate_binary_file, '.mind'), 
	(generate_protobuf_file, '.mind.gz')
	])
def userfile(request, tmp_path):
	'''
	Returns a userfile containing user info and a single snapshot.
	'''
	generate, extension = request.param
	path = tmp_path / f"userfile{extension}"
	generate(path)
	return path


def test_reader(userfile):
	if userfile.name.endswith(".gz"):
		r = reader.Reader(userfile, "protobuf")
	else:
		r = reader.Reader(userfile, "binary")
	assert r.user_id == tu._USER_ID
	assert r.user_name == tu._USERNAME
	assert r.birth_date == tu._BIRTHDAY
	assert r.gender == gender_dict[tu._GENDER]
	snap = next(iter(r))
	assert snap.datetime == tu._DATETIME
	assert (snap.translation == 
		(tu._TRANSLATION_X, tu._TRANSLATION_Y, tu._TRANSLATION_Z))
	assert (snap.rotation == (tu._ROTATION_X,
		tu._ROTATION_Y, tu._ROTATION_Z, tu._ROTATION_W))
	assert snap.c_height == tu._C_HEIGHT
	assert snap.c_width == tu._C_WIDTH
	assert snap.color_image.data == tu._C_DATA
	assert snap.d_height == tu._D_HEIGHT
	assert snap.d_width == tu._D_WIDTH
	d_bytes = struct.pack(f"{len(tu._D_DATA)}f", *tu._D_DATA)
	assert snap.depth_image.data == d_bytes
	assert snap.hunger == tu._HUNGER
	assert snap.thirst == tu._THIRST
	assert snap.exhaustion == tu._EXHAUSTION
	assert snap.happiness == tu._HAPPINESS
