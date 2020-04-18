import struct
import os
from PIL import Image
from datetime import datetime
import io
from ..protobufs import cortex_pb2


_SNP_FORMAT = "Snapshot from {0} at {1} on {2} / {3} with a {4}x{5} color \
image and a {6}x{7} depth image."


class Snapshot:
	def __init__(self, datetime, translation, rotation, c_height, 
		c_width, color_image, d_height, d_width, depth_image,
		hunger, thirst, exhaustion ,happiness):
		self.datetime = datetime
		self.translation = translation
		self.rotation = rotation
		self.c_height = c_height
		self.c_width = c_width
		self.color_image = color_image
		self.d_height = d_height
		self.d_width = d_width
		self.depth_image = depth_image
		self.hunger = hunger
		self.thirst = thirst
		self.exhaustion = exhaustion
		self.happiness = happiness

	def __str__(self):
		# self.datetime is in milliseconds.
		dttime = datetime.fromtimestamp(self.datetime / 1000)
		fmt_date = dttime.strftime("%B %d, %Y")
		fmt_time = dttime.strftime("%I:%M:%S.%f")
		return _SNP_FORMAT.format(fmt_date, fmt_time, self.translation,\
			self.rotation, self.c_height, self.c_width, \
			self.d_height, self.d_width)


	@classmethod
	def from_stream(cls, stream):
		"""
		Initializes a snapshot by reading its data from a bytes iterator.
		"""
		datetime = struct.unpack("Q", stream.read(8))[0]
		translation = struct.unpack("ddd", stream.read(24))	# A 3-tuple.
		rotation = struct.unpack("dddd", stream.read(32))	# A 4-tuple.
		c_height, c_width = struct.unpack("II", stream.read(8))
		print("Reading bgr image.")
		bgr = read_data(stream, 3 * c_height * c_width)
		# We need to flip the image data from bgr to rgb
		temp_image = Image.frombytes('RGB', (c_width, c_height), bgr)
		b, g, r = temp_image.split()
		temp_image = Image.merge('RGB', (r, g, b))
		rgb = temp_image.tobytes()
		color_image = ImageData("color", c_width, c_height, rgb)
		d_height, d_width = struct.unpack("II", stream.read(8))
		depths = read_data(stream, 4 * d_height * d_width)
		print(f"Size of depth_image data is {len(depths)}")
		depth_image = ImageData("depth", d_width, d_height, depths)
		hunger, thirst = struct.unpack("ff", stream.read(8))
		exhaustion, happiness = struct.unpack("ff", stream.read(8))
		return cls(datetime, translation, rotation, c_height,
			c_width, color_image, d_height, d_width, depth_image,
			hunger, thirst, exhaustion, happiness)

	@classmethod
	def from_proto_stream(cls, stream):
		"""
		Initializes a snapshot by reading its data from a protobuf
		formatted bytes iterator.
		"""
		message_len = int.from_bytes(stream.read(4), byteorder="little")
		snp = cortex_pb2.Snapshot()
		snp.ParseFromString(stream.read(message_len))
		datetime = snp.datetime
		translation = (snp.pose.translation.x, snp.pose.translation.y,
			snp.pose.translation.z)
		rotation = (snp.pose.rotation.x, snp.pose.rotation.y,
			snp.pose.rotation.z, snp.pose.rotation.w)
		c_width = snp.color_image.width
		c_height = snp.color_image.height
		color_image = ImageData('color', snp.color_image.width,
			snp.color_image.height, snp.color_image.data)
		d_width = snp.depth_image.width
		d_height = snp.depth_image.height
		depths = struct.pack(f"{len(snp.depth_image.data)}f",
			*snp.depth_image.data)
		depth_image = ImageData('depth', snp.depth_image.width,
			snp.depth_image.height, depths)
		hunger = snp.feelings.hunger
		thirst = snp.feelings.thirst
		exhaustion = snp.feelings.exhaustion
		happiness = snp.feelings.happiness
		return cls(datetime, translation, rotation, c_height,
			c_width, color_image, d_height, d_width, depth_image,
			hunger, thirst, exhaustion, happiness)



	@classmethod
	def from_bytes(cls, bytes):
		"""
		Initializes a snapshot by reading its data from a bytes object.
		"""
		stream = io.BytesIO(bytes)
		return cls.from_stream(stream)

	@classmethod
	def deserialize(cls, data):
		stream = iter(data)
		return cls.from_stream(stream)

	def serialize_request(self, fields):
		msg = struct.pack("Q", self.datetime)
		if "pose" in fields:
			msg += struct.pack("ddd", *self.translation)
			msg += struct.pack("dddd", *self.rotation)
		else:
			msg += struct.pack("ddd", 0, 0, 0)
			msg += struct.pack("dddd", 0, 0, 0, 0)
		'''
		if "translation" in fields:
			msg += struct.pack("ddd", *self.translation)
		else:
			msg += struct.pack("ddd", 0, 0, 0)
		if "rotation" in fields:
			msg += struct.pack("dddd", *self.rotation)
		else:
			msg += struct.pack("dddd", 0, 0, 0, 0)
		'''
		if "color_image" in fields:
			msg += struct.pack("II", self.c_height, self.c_width)
			msg += self.color_image.data
		else:
			msg += struct.pack("II", 0, 0)
		if "depth_image" in fields:
			msg += struct.pack("II", self.d_height, self.d_width)
			data = self.depth_image.data[:] # Protobuf lists are very weird :P
			msg += struct.pack('%sf' % len(data), *data)
		else:
			msg += struct.pack("II", 0, 0)
		if "feelings" in fields:
			msg += struct.pack("ff", self.hunger, self.thirst)
			msg += struct.pack("ff", self.exhaustion, self.happiness)
		else:
			msg += struct.pack("ffff", 0, 0, 0, 0)
		return msg

	def serialize(self):
		all_fields = ["translation", "rotation", "color_image", 
		"depth_image", "feelings"]
		return self.serialize_request(all_fields)



def read_data(stream, size):
	print(f"I have to read {size} bytes of data.")
	size_left = size
	data = b''
	while size_left >= 1000000:
		#print("Just read a 1000000 bytes.")
		data += stream.read(1000000)
		size_left -= 1000000
	data += stream.read(size_left)
	return data


class ImageData:
	def __init__(self, fmt, width, height, data):
		self.fmt = fmt
		self.width = width
		self.height = height
		# If image format is color, we need to flip the data from BGR to RGB.
		if fmt == "color":
			self.data = data
			self.size = width * height * 3
		else:
			self.data = data
			self.size = width * height * 4

