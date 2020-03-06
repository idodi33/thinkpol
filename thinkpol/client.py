import datetime
from .utils import connection as cn
from . import thought as tht
from .utils import reader
#from .utils import protocol
import time
import cortex_pb2
import config_pb2

def upload_snapshots(file_name, address):
	r = reader.Reader(file_name, 'binary')
	'''
	hello = protocol.Hello(r.user_id, r.user_name, r.birth_date, r.gender)
	hello_msg = hello.serialize()
	'''
	user = cortex_pb2.User(
		user_id = r.user_id,
		username = r.user_name,
		birthday = r.birth_date,
		gender = r.gender.upper()
		)
	user_msg = user.SerializeToString()
	if type(address) == str:
		ip, port = address.split(':')
	else:	# it's a tuple
		ip, port = address
	for snapshot in r:
		time.sleep(0.5)
		with cn.Connection.connect(ip, int(port)) as connection:
			connection.send_message(user_msg)
			config_msg = connection.receive_message()
			config = config_pb2.Config()
			config.ParseFromString(config_msg)
			#config = protocol.Config.deserialize(config_msg)
			snapshot_msg = snapshot.serialize_request(config.fields)
			connection.send_message(snapshot_msg)


def upload_thought(address, user, thought):
    # Form the message according to the protocol.
    thought_obj = tht.Thought(user, datetime.datetime.now(), thought)
    msg = thought_obj.serialize()
    if type(address) == str:
        ip, port = address.split(':')
    else: # it's a tuple
        ip, port = address
    with cn.Connection.connect(ip, int(port)) as connection:
        connection.send(msg)
