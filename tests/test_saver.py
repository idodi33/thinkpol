import pytest
import furl
import time
import json
from thinkpol import saver
import tester_utils as tu


jsons_dict = {
	"color_image": tu._C_IMAGE_JSON,
	"depth_image": tu._D_IMAGE_JSON,
	"pose": tu._POSE_JSON,
	"feelings": tu._FEELINGS_JSON
}


def test_saver_save():
	url = furl.furl()
	url.host = tu._HOST
	url.port = tu._DB_PORT
	url.scheme = tu._DB
	s = saver.Saver(url)
	for name, js in jsons_dict.items():
		s.save(name, js)
	time.sleep(1)
	db = s.database
	assert tu._USERNAME == json.loads(db.find('users'))[0]['username']
	assert tu._BIRTHDAY == json.loads(
		db.find('user', user_id=tu._USER_ID)
		)[0]['birthday']
	assert tu.server_gender_dict[tu._GENDER] == json.loads(
		db.find('user', user_id=tu._USER_ID)
		)[0]['gender']
	assert tu._USER_ID == json.loads(
		db.find('user', user_id=tu._USER_ID)
		)[0]['user_id']
	assert (tu._DATETIME == json.loads(
		db.find('snapshots', user_id=tu._USER_ID)
		)[0]['datetime'])
	assert (tu._DATETIME == json.loads(
		db.find('snapshot', user_id=tu._USER_ID, snapshot_id=tu._DATETIME)
		)[0]['datetime'])
	for name, js in jsons_dict.items():
		result = db.find('result',
			user_id=tu._USER_ID,
			snapshot_id=tu._DATETIME,
			result_name=name
			)
		result_dict = json.loads(result)[0]
		del result_dict['_id']
		assert all(item in json.loads(js).items() 	# that the second dict is a subset of the first
			for item in result_dict.items())


"""
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
				DataBase.result_to_dict(result_name))"""
