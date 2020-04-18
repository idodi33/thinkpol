import os
import pathlib
import threading
import json
from datetime import datetime

DATA_DIR = os.path.join(os.getcwd(), 'parsed_data')


lock = threading.Lock()

def get_file_path(snapshot, type):
	"""
	Gets a snapshot and returns file paths for the parsed color/depth image (depending on type).
	"""
	json_snap = json.loads(snapshot)
	datetime_obj = datetime.fromtimestamp(json_snap['datetime'] / 1000)
	formatted_time = datetime.strftime( datetime_obj, "%Y-%m-%d_%H-%M-%S-%f")
	
	with lock:
		subdir_pathname = os.path.join(DATA_DIR , formatted_time)
		subdir_path = pathlib.Path(subdir_pathname)
		if not subdir_path.is_dir():
			subdir_path.mkdir(parents=True)
		if type == 'color':
			file_pathname = os.path.join(subdir_pathname, "color_image.jpg")
		elif type == 'depth':
			file_pathname = os.path.join(subdir_pathname, "depth_image.jpg")
		else:
			raise ValueError('Invalid file type.')
		file_path = pathlib.Path(file_pathname)
		if not file_path.is_file():
			file_path.touch()
		return file_path

def extract_metadata(json_snap):
	'''
	Gets a dictionary with snapshot data and returns a
	dictionary containing only data about the user.
	'''
	metadata = {
		'user_id' : json_snap['user_id'],
		'username' : json_snap['username'],
		'birthday' : json_snap['birthday'],
		'gender' : json_snap['gender'],
		'datetime' : json_snap['datetime']
	}
	return metadata