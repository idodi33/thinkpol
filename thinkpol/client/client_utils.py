from thinkpol.utils import connection as cn
from thinkpol.protobufs import cortex_pb2
from thinkpol.protobufs import config_pb2


def get_user_msg(r):
	"""
	Gets a formatted binary message containing user information
	from a reader object.

	:param r: the reader object
	:type r: Reader
	:returns: the formatted binary message
	:rtype: bytes
	"""
	user = cortex_pb2.User(
		user_id = r.user_id,
		username = r.user_name,
		birthday = r.birth_date,
		gender = r.gender
		)
	user_msg = user.SerializeToString()
	return user_msg


def send_snapshot(user_msg, snapshot, host, port):
	"""
	Sends a single snapshot of a user's cognition 
	to server in address host:port.

	:param user_msg: the serialized binary info of the user who's snapshot we're to send
	:type user_msg: bytes 
	:param snapshot: the snapshot we're to send
	:type snapshot: Snapshot
	:param host: the host of the server
	:type host: str
	:param port: the port of the server
	:type port: str
	"""
	with cn.Connection.connect(host, int(port)) as connection:
		connection.send_message(user_msg)
		config_msg = connection.receive_message()
		config = config_pb2.Config()
		config.ParseFromString(config_msg)
		snapshot_msg = snapshot.serialize_request(
			config.fields
			)
		connection.send_message(snapshot_msg)