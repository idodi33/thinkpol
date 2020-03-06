import struct
import io
import protocol_pb2.py



"""
class Hello:
	def __init__(self, user_id, user_name, birth_date, gender):
		self.user_id = user_id
		self.user_name = user_name
		self.birth_date = birth_date
		self.gender = gender

	def serialize(self):
		msg = struct.pack("Q", self.user_id)
		name_length = len(self.user_name)
		msg += struct.pack("I", name_length)
		msg += self.user_name.encode("utf-8")
		msg += struct.pack("I", self.birth_date)
		msg += self.gender.encode("utf-8")
		return msg

	@classmethod
	def deserialize(cls, data):
		stream = io.BytesIO(data)
		user_id = struct.unpack("Q", stream.read(8))[0]
		name_length = struct.unpack("I", stream.read(4))[0]
		encoded_user_name = stream.read(name_length)
		user_name = encoded_user_name.decode("utf-8")
		birth_date = struct.unpack("I", stream.read(4))[0]
		encoded_gender = stream.read(1)
		gender = encoded_gender.decode("utf-8")
		return Hello(user_id, user_name, birth_date, gender)

class Config:
	def __init__(self, fields):
		self.fields = fields

	def serialize(self):
		num_fields = len(self.fields)
		msg = struct.pack("I", num_fields)
		for field in self.fields:
			field_len = len(field)
			msg += struct.pack("I", field_len)
			msg += field.encode("utf-8")
		return msg

	@classmethod
	def deserialize(cls, data):
		stream = io.BytesIO(data)
		num_fields = struct.unpack("I", stream.read(4))[0]
		fields = []
		for i in range(num_fields):
			field_len = struct.unpack("I", stream.read(4))[0]
			encoded_field = stream.read(field_len)
			field = encoded_field.decode("utf-8")
			fields.append(field)
		return Config(fields)
"""