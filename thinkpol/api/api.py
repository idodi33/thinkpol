from flask import *
from pymongo import *
import json
from flask_cors import CORS, cross_origin


api = Flask(__name__)
CORS(api)	# this enables our GUI webserver to send http requests here

class API:
	def __init__(self, host, port, database):
		API.host = host
		API.port = port
		API.database = database
		API.api = api


@api.route('/users')
def handle_users():
	return API.database.find('users')


@api.route('/users/<int:user_id>')
def handle_user(user_id):
	return API.database.find('user', user_id=user_id)


@api.route('/users/<int:user_id>/snapshots')
def handle_snapshots(user_id):
	return API.database.find('snapshots', user_id=user_id)


@api.route('/users/<int:user_id>/snapshots/<int:snapshot_id>')
def handle_snapshot(user_id, snapshot_id):
	return API.database.find('snapshot', 
		user_id=user_id, snapshot_id=snapshot_id)


@api.route('/users/<int:user_id>/snapshots/<int:snapshot_id>/<result_name>')
def handle_result(user_id, snapshot_id, result_name):
	return API.database.find('result', user_id=user_id,
	snapshot_id=snapshot_id, result_name=result_name)

@api.route('/users/<int:user_id>/snapshots/<int:snapshot_id>/<result_name>/data')
def handle_result_data(user_id, snapshot_id, result_name):
	bytes_dict = handle_result(user_id, snapshot_id, result_name)
	json_dict = json.loads(bytes_dict)[0]
	path = json_dict[result_name]	# this would be either color_image or depth_image
	with open(path, 'rb') as f:
		return f.read()