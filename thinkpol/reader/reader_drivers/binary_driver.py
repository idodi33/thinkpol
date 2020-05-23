import struct
import os
from thinkpol.utils.snapshot import Snapshot


class BinaryDriver:
	"""
	Reads formatted binary data from a given file.

	:param file_name: the name of the file
	:type file_name: str
	:param offset: the amount of bytes already read from the file
	:type offset: int
	"""

	field = 'binary'

	def __init__(self, file_name):
		self.file_name = file_name
		self.offset = 0

	def get_user_info(self):
		"""
		Reads user info from the given file.

		:returns: a 4-tuple - (user_id, user_name, birth_date, gender), containing user data.
		:rtype: tuple
		"""
		with open(self.file_name, 'rb') as f:
			print("started parsing user info")
			user_id, name_length = struct.unpack("QI", f.read(12))
			encoded_user_name = f.read(name_length)
			print("Reading user info some more")
			user_name = encoded_user_name.decode("utf-8")
			birth_date = struct.unpack("I", f.read(4))[0]
			gender_dict = {'m':0, 'f':1, 'o': 2}
			gender_char = f.read(1).decode("utf-8")
			gender = gender_dict[gender_char]
			print("Readinggg")
			self.offset = 17 + name_length
			return user_id, user_name, birth_date, gender


	def get_snap_iterator(self):
		"""
		Reads snapshots from the given file iteratively.
		"""
		with open(self.file_name, 'rb') as f:
			f.read(self.offset)
			file_position = f.tell()
			f.seek(0, os.SEEK_END)
			file_end = f.tell()
			f.seek(file_position, os.SEEK_SET)
			while f.tell() != file_end:
				yield Snapshot.from_stream(f)

