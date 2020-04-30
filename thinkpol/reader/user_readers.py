from ..protobufs import cortex_pb2
import gzip
import struct


def binary_user_info(file_name):
	"""
	Recieves a binary file name and reads user info from it.

	:param file_name: name of the file
	:type file_name: str
	:returns: a 5-tuple - (user_id, user_name, birth_date, gender, offset),
	where the first four are user data and 'offset' is the length 
	of the user data in the file.
	:rtype: tuple
	"""
	with open(file_name, 'rb') as f:
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
		offset = 17 + name_length
		return user_id, user_name, birth_date, gender, offset


def protobuf_user_info(file_name):
	"""
	Recieves a protobuf file name and reads user info from it.

	:returns: a 5-tuple - (user_id, user_name, birth_date, gender, offset),
	where the first four are user data, 
	and offset is the length of the user data
	in the file.
	:rtype: tuple
	"""
	with gzip.open(file_name, 'rb') as f:
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
		offset = message_size + 4
		return user_id, user_name, birth_date, gender, offset


user_readers = {
	'binary': binary_user_info, 
	'protobuf': protobuf_user_info
	}