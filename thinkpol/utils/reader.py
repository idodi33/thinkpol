import struct
import os
from .snapshot import Snapshot
from datetime import datetime
from ..protobufs import cortex_pb2

_USR_FORMAT = "user {0}: {1}, born {2} ({3})"


def binary_user_info(f):
	"""
	Recieves a binary file object and reads user info from it.
	"""
	print("started parsing user info")
	user_id, name_length = struct.unpack("QI", f.read(12))
	encoded_user_name = f.read(name_length)
	print("Reading user info some more")
	user_name = encoded_user_name.decode("utf-8")
	birth_date = struct.unpack("I", f.read(4))[0]
	gender_dict = {'m':'male', 'f':'female', 'o': 'other'}
	gender_char = f.read(1).decode("utf-8")
	gender = gender_dict[gender_char]
	print("Readinggg")
	offset = 17 + name_length
	return user_id, user_name, birth_date, gender, offset


def protobuf_user_info(f):
	"""
	Recieves a binary file object and reads user info from it.
	"""
	message_size = int.from_bytes(f.read(4))
	user = cortex_pb2.User()
	user.ParseFromString(f.read(message_size))
	user_id = user.user_id
	user_name = user.user_name
	birth_date = user.birthday
	gender_dict = {0: "male", 1: "female", 2: "other"}
	gender = gender_dict[user.gender]
	offset = message_size + 4
	return user_id, user_name, birth_date, gender, offset


user_funcs = {'binary': binary_user_info, 'protobuf': protobuf_user_info}


class Reader:
	def __init__(self, file_name, format):
		print("Currently reading file")
		self.format = format
		with open(file_name, 'rb') as f:
			for format_name, func in user_funcs.items():
				if format_name == self.format:
					user_info = func(f)
					break
			else:
				raise ValueError(f'Invalid format: {self.format}')
			self.user_id, self.user_name, self.birth_date, \
			self.gender, offset = user_info 
		self.snapshots_iterator = Reader.iter_snapshots(file_name, offset, format)
		print("Done with reader init")

	def __str__(self):
		dttime = datetime.fromtimestamp(self.birth_date)
		fmt_date = dttime.strftime("%B %d, %Y")
		data = _USR_FORMAT.format(self.user_id, self.user_name,\
			fmt_date, self.gender)
		return data


	@classmethod
	def iter_snapshots(cls, file_name, offset, format):
		"""
		Recieves a file name and reads snapshots from it iteratively.
		offset marks the length of the user info in the file.
		"""
		with open(file_name, 'rb') as f:
			f.read(offset)
			file_position = f.tell()
			f.seek(0, os.SEEK_END)
			file_end = f.tell()
			f.seek(file_position, os.SEEK_SET)
			if format == 'binary':
				while f.tell() != file_end:
					yield Snapshot.from_stream(f)
			else:	# self.format == 'protobuf'
				while f.tell != file.end:
					yield Snapshot.from_proto_stream(f)

	def __iter__(self):
		return iter(self.snapshots_iterator)








