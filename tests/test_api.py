import pytest
import thinkpol.api.api
import json
import tester_utils as tu


class MockDB:
	def find(self, request, user_id=None, snapshot_id=None, result_name=None):
		if request == "users":
			return {tu._USER_ID : tu._USER_DICT}
		elif request == "user":
			assert user_id == tu._USER_ID
			return tu._USER_DICT
		elif request == "snapshots":
			assert user_id == tu._USER_ID
			return {user_id : "snapshots"}
		elif request == "snapshot":
			assert user_id == tu._USER_ID
			assert snapshot_id == tu._DATETIME
			return {snapshot_id : "snapshot"}
		elif request == "result":
			assert user_id == tu._USER_ID
			assert snapshot_id == tu._DATETIME
			result_dict = {result_name : result_name}
			return result_dict


class MockAPI:
	'''
    This replaces the normal API class api.py uses.
	'''
	host = "0.0.0.0"
	port = 5000
	database = MockDB()
	api = thinkpol.api.api.api


@pytest.fixture
def mock_db(monkeypatch):
	monkeypatch.setattr(thinkpol.api.api, 'API', MockAPI)


def test_users(mock_db):
	with thinkpol.api.api.api.test_client() as c:
		response = c.get('/users')
		assert response.get_json() == {str(tu._USER_ID) : tu._USER_DICT}


def test_user(mock_db):
	with thinkpol.api.api.api.test_client() as c:
		response = c.get('/users/' + str(tu._USER_ID))
		assert response.get_json() == tu._USER_DICT


def test_snapshots(mock_db):
	with thinkpol.api.api.api.test_client() as c:
		response = c.get('/users/' + str(tu._USER_ID) + "/snapshots")
		assert response.get_json() == {str(tu._USER_ID) : "snapshots"}


def test_snapshot(mock_db):
	with thinkpol.api.api.api.test_client() as c:
		response = c.get('/users/' + str(tu._USER_ID) + "/snapshots/" + str(tu._DATETIME))
		assert response.get_json() == {str(tu._DATETIME) : "snapshot"}


def test_result(mock_db):
	with thinkpol.api.api.api.test_client() as c:
		for field in ['color_image', 'depth_image', 'pose', 'feelings']:
			response = c.get('/users/' + str(tu._USER_ID) + "/snapshots/" + str(tu._DATETIME) + "/" + field)
			assert response.get_json() == {field : field}


