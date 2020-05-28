from pymongo import *
import json
import bson.json_util

class DataBase:
	"""
	Saves and reads formatted data from a specified mongodb database.

	:param host: the host of the db connection, defaults to 'localhost'
	:type host: str, optional
	:param port: the port of the db connection, defaults to 27017
	:type port: int, optional
	"""
	def __init__(self, host='localhost', port=27017):
		self.client = MongoClient(host=host, port=port)
		self.db = self.client.db
		self.users = self.db.users
		self.snapshots = self.db.snapshots


	def save(self, field, data):
		"""
		Gets a json with data from parser and saves it into the database.

		:param field: the field of snapshot data that the json contains
		:type field: str
		:param data: the snapshot data
		:type data: json
		:raises: ValueError
		"""
		data = json.loads(data)
		self.users.update_one({'user_id': data['user_id']},
			{'$set': {'user_id': data['user_id'],
			'username': data['username'],
			'birthday': data['birthday'],
			'gender': data['gender']}
			},
			True	# upsert
			)
		if field == "color_image":
			update = {'color_image': data['color_image']}
		elif field == "depth_image":
			update = {'depth_image': data['depth_image']}
		elif field == "pose":
			update = {
				'translation_x': data['translation_x'],
				'translation_y': data['translation_y'],
				'translation_z': data['translation_z'],
				'rotation_x': data['rotation_x'],
				'rotation_y': data['rotation_y'],
				'rotation_z': data['rotation_z'],
				'rotation_w': data['rotation_w']
				}
		elif field == "feelings":
			update = {
				'happiness': data['happiness'],
				'exhaustion': data['exhaustion'],
				'hunger': data['hunger'],
				'thirst': data['thirst']
				}
		else:
			raise ValueError("Error in mongodb driver save: Invalid field")
		update.update({
			'datetime': data['datetime'], 
			'parent_user_id': data['user_id']
			})
		data_dict = {'$set': update}
		self.snapshots.update_one(
			{'datetime': data['datetime']}, data_dict, True	# upsert
			)


	def find(self, request, user_id=None, snapshot_id=None, result_name=None):
		"""
		Gets a find request and returns the matching data from the database.

		:param request: type of request ('users'/'user'/'snapshots'/'snapshot'/'result')
		:type request: str
		:param user_id: id of the desired user, defaults to None
		:type user_id: int, optional
		:param snapshot_id: id (datetime in seconds) of the specified snapshot, defaults to None
		:type snapshot_id: int, optional
		:param result_name: field of desired data, defaults to None
		:type result_name: str, optional
		:returns: json containing the data as pulled from the database
		:rtype: json
		:raises: ValueError
		"""
		if request == 'users':
			ret = self.users.find({}, {'user_id': 1, 'username' : 1})
		elif request == 'user':
			ret = self.users.find({'user_id': user_id})
		elif request == 'snapshots':
			ret = self.snapshots.find(
				{'parent_user_id':user_id}, 
				{'parent_user_id': 1, 'datetime': 1}
				)
		elif request == 'snapshot':
			ret = self.snapshots.find({
				'parent_user_id': user_id, 
				'datetime': snapshot_id}
				)
		elif request == 'result':
			ret = self.snapshots.find(
				{'parent_user_id': user_id, 'datetime': snapshot_id}, 
				DataBase.result_to_dict(result_name))
		else:
			raise ValueError("Error in mongodb driver find: Invalid field")
		return bson.json_util.dumps(ret)	# this turns a cursor object, returned by find, to json

	@staticmethod
	def result_to_dict(result_name):
		'''
		Takes a result name (pose, color_image, etc.) and returns a mongo dict
		requesting only the fields that belong to that result type.
		'''
		if result_name == "color_image":
			find = {'color_image': 1}
		elif result_name == "depth_image":
			find = {'depth_image': 1}
		elif result_name == "pose":
			find = {
				'translation_x': 1,
				'translation_y': 1,
				'translation_z': 1,
				'rotation_x': 1,
				'rotation_y': 1,
				'rotation_z': 1,
				'rotation_w': 1
				}
		elif result_name == "feelings":
			find = {
				'datetime': 1,
				'happiness': 1,
				'exhaustion': 1,
				'hunger': 1,
				'thirst': 1
				}
		else:
			raise ValueError("Error in mongodb driver find: Invalid result name")
		return find