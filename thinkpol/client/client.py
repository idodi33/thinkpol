import datetime
from thinkpol.client.client_utils import get_user_msg, send_snapshot
from thinkpol.reader import reader
#from .utils import protocol
import time


def upload_sample(host, port, path):
	"""
	Accepts a host address, a port and a file name and uploads cognition snapshots
	from the file to the specified address.

	:param host: the host we send the data to
	:type host: str
	:param port: the port we send the data to
	:type port: int
	:param path: the path of the file we process
	:type path: str
	"""
	address = (host, port)
	if path.endswith('.gz'):
		r = reader.Reader(path, 'protobuf')
	else:
		r = reader.Reader(path, 'binary')
	user_msg = get_user_msg(r)
	if type(address) == str:
		host, port = address.split(':')
	else:	# it's a tuple
		host, port = address
	for snapshot in r:
		time.sleep(0.5)
		send_snapshot(user_msg, snapshot, host, port)

