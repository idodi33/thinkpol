from flask import *
from pymongo import *
import json
from flask_cors import CORS, cross_origin


api = Flask(__name__)
CORS(api)	# this enables our GUI webserver to send http requests here

class API:
	"""
	An object that holds the relevant data for taking data from a 
	database and displaying it through an API.

	:param host: the API connection's host
	:type host: str
	:param port: the API connection's port
	:type port: int
	:param database: the database
	:type database: DataBase
	"""
	def __init__(self, host, port, database):
		API.host = host
		API.port = port
		API.database = database
		API.api = api


@api.route('/users')
def handle_users():
	"""
	Handles a request to see data about all users.

	:returns: data about all users
	:rtype: json
	"""
	return API.database.find('users')


@api.route('/users/<int:user_id>')
def handle_user(user_id):
	"""
	Handles a request to see data about a specific user.

	:param user_id: the desired user's id
	:type user_id: int
	:returns: data about the desired user
	:rtype: json
	"""
	return API.database.find('user', user_id=user_id)


@api.route('/users/<int:user_id>/snapshots')
def handle_snapshots(user_id):
	"""
	Handles a request to see data about a specific user's snapshots.
	
	:param user_id: the desired user's id
	:type user_id: int
	:returns: data about the desired user's snapshots
	:rtype: json
	"""
	return API.database.find('snapshots', user_id=user_id)


@api.route('/users/<int:user_id>/snapshots/<int:snapshot_id>')
def handle_snapshot(user_id, snapshot_id):
	"""
	Handles a request to see data about a specific user's snapshot.
	:param user_id: the desired user's id
	:type user_id: int
	:param snapshot_id: the desired snapshot's id (datetime in seconds)
	:type snapshot_id: int
	:returns: data about the desired snapshot
	:rtype: json
	"""
	return API.database.find('snapshot', 
		user_id=user_id, snapshot_id=snapshot_id)


@api.route('/users/<int:user_id>/snapshots/<int:snapshot_id>/<result_name>')
def handle_result(user_id, snapshot_id, result_name):
	"""
	Handles a request to see data about a specific field in a snapshot.

	:param user_id: the desired user's id
	:type user_id: int
	:param snapshot_id: the desired snapshot's id (datetime in seconds)
	:type snapshot_id: int
	:param result_name: the field of the desired result
	:type result_name: str
	:returns: data about the desired snapshot
	:rtype: json
	"""
	return API.database.find('result', user_id=user_id,
	snapshot_id=snapshot_id, result_name=result_name)


@api.route('/users/<int:user_id>/snapshots/<int:snapshot_id>/<result_name>/data')
def handle_result_data(user_id, snapshot_id, result_name):
	"""
	Handles a request to see binary data associated with 
	a specific field in a snapshot.

	:param user_id: the desired user's id
	:type user_id: int
	:param snapshot_id: the desired snapshot's id (datetime in seconds)
	:type snapshot_id: int
	:param result_name: the field of the desired result
	:type result_name: str
	:returns: data about the desired snapshot
	:rtype: json
	"""
	bytes_dict = handle_result(user_id, snapshot_id, result_name)
	json_dict = json.loads(bytes_dict)[0]
	path = json_dict[result_name]	# this would be either color_image or depth_image
	with open(path, 'rb') as f:
		return f.read()