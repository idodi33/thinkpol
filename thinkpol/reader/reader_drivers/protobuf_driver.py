from thinkpol.protobufs import cortex_pb2
from thinkpol.utils.snapshot import Snapshot
import gzip
import os


class ProtobufDriver:
	"""
	Reads formatted gzipped protobuf data from a given file.

	:param file_name: the name of the file
	:type file_name: str
	:param offset: the amount of bytes already read from the file
	:type offset: int
	"""

	field = "protobuf"

	def __init__(self, file_name):
		self.file_name = file_name
		self.offset = 0

	def get_user_info(self):
		"""
		Reads user info from the given file.

		:returns: a 4-tuple - (user_id, user_name, birth_date, gender), containing user data.
		:rtype: tuple
		"""
		with gzip.open(self.file_name, 'rb') as f:
			message_size = int.from_bytes(
				f.read(4), 
				byteorder="little"
				)
			user = cortex_pb2.User()
			user.ParseFromString(f.read(message_size))
			user_id = user.user_id
			user_name = user.username
			birth_date = user.birthday
			gender = user.gender
			#gender_dict = {0: "man", 1: "woman", 2: "other"}
			#gender = gender_dict[user.gender]
			print(f"Gender is {gender}")
			self.offset = message_size + 4
			return user_id, user_name, birth_date, gender

	def get_snap_iterator(self):
		"""
		Reads snapshots from the given file iteratively.
		"""
		with gzip.open(self.file_name, 'rb') as f:
			f.read(self.offset)
			file_position = f.tell()
			f.seek(0, os.SEEK_END)
			file_end = f.tell()
			f.seek(file_position, os.SEEK_SET)
			while f.tell != file_end:
				yield Snapshot.from_proto_stream(f)