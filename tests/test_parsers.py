import pytest
import json
from datetime import datetime
import thinkpol.parsers
import tester_utils as tu

'''
@pytest.fixture
def mock_data_dir(monkeypatch, tmp_path):
	monkeypatch.setattr('thinkpol.parsers.parser_utils.DATA_DIR', tmp_path)
'''

def assert_user_info(field, path=None):
	#print(f"assert_user_info: DATA_DIR is {parsers.parser_utils.DATA_DIR}")
	parser = thinkpol.parsers.parsers[field]
	js = parser(tu._JSON, path)
	js_dict = json.loads(js)
	assert js_dict['username'] == tu._USERNAME
	assert js_dict['user_id'] == tu._USER_ID
	assert js_dict['birthday'] == tu._BIRTHDAY
	assert js_dict['gender'] == tu.server_gender_dict[tu._GENDER]
	return js_dict


@pytest.mark.parametrize(
	"format", [
	('color_image'), ('depth_image')]
	)
def test_image(tmp_path, format):
	js_dict = assert_user_info(format, tmp_path)
	datetime_obj = datetime.fromtimestamp(tu._DATETIME / 1000)
	print(f"datetime_obj: {datetime_obj}")
	formatted_time = datetime.strftime( datetime_obj, "%Y-%m-%d_%H-%M-%S-%f")
	file_path = tmp_path / formatted_time / (format + ".jpg")
	print(f"file_path: {file_path}")
	print(f"data was saved at: {js_dict[format]}")
	#assert js_dict[format] == str(file_path.resolve())
	with open(file_path, 'rb') as f:
		if format == 'color_image':
			assert f.read() == tu._PARSED_C_DATA
		else:
			data = f.read()
			assert data == tu._PARSED_D_DATA


def test_pose():
	js_dict = assert_user_info('pose')
	assert js_dict['translation_x'] == tu._TRANSLATION_X
	assert js_dict['translation_y'] == tu._TRANSLATION_Y
	assert js_dict['translation_z'] == tu._TRANSLATION_Z
	assert js_dict['rotation_x'] == tu._ROTATION_X
	assert js_dict['rotation_y'] == tu._ROTATION_Y
	assert js_dict['rotation_z'] == tu._ROTATION_Z
	assert js_dict['rotation_w'] == tu._ROTATION_W


def test_feelings():
	js_dict = assert_user_info('feelings')
	assert js_dict['hunger'] == tu._HUNGER
	assert js_dict['thirst'] == tu._THIRST
	assert js_dict['exhaustion'] == tu._EXHAUSTION
	assert js_dict['happiness'] == tu._HAPPINESS

