from pymongo import *
import json
import bson.json_util

class DataBase:
	def __init__(self, host='localhost', port=27017):
		self.client = MongoClient(host=host, port=port)
		self.db = self.client.db
		self.users = self.db.users
		self.snapshots = self.db.snapshots


	def save(self, field, data):
		'''
		Gets a json with data from parser and saves it into the database.
		'''
		data = json.loads(data)
		print(f"mdb_driver: data to be saved is {data}")
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
		update.update({'datetime': data['datetime'], 'parent_user_id': data['user_id']})
		print(f'update is: {update}')
		data_dict = {'$set': update}
		print(f"data dict is {data_dict}")
		self.snapshots.update_one({'datetime': data['datetime']}, data_dict,
			True	# upsert
			)
		print("mdb_driver: saved message")


	def find(self, request, user_id=None, snapshot_id=None, result_name=None):
		'''
		Gets a find request of the type 'users'/'user'/'snapshots'/'snapshot'/'result'
		and returns the matching data from the database.
		'''
		#user_id = None if user_id is None else int(user_id)
		#snapshot_id = None if snapshot_id is None else int(snapshot_id)
		if request == 'users':
			ret = self.users.find({}, {'user_id': 1, 'username' : 1})
		elif request == 'user':
			ret = self.users.find({'user_id': user_id})
		elif request == 'snapshots':
			ret = self.snapshots.find({'parent_user_id':user_id}, {'parent_user_id': 1, 'datetime': 1})
		elif request == 'snapshot':
			ret = self.snapshots.find({'parent_user_id': user_id, 'datetime': snapshot_id})
		elif request == 'result':
			ret = self.snapshots.find({'parent_user_id': user_id, 'datetime': snapshot_id}, 
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