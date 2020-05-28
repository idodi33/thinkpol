"""
A collection of common utilities used by one or more of the parsers.

:param DATA_DIR: the directory in which that parsed images
are saved by default
:type DATA_DIR: str
:param lock: a threading lock used by the get_file_path function
to make sure images are saved properly
:type lock: Lock
"""
import os
import pathlib
import threading
import json
from datetime import datetime


#DATA_DIR = os.path.join(os.getcwd(), 'parsed_data')
DATA_DIR = pathlib.Path("opt/thinkpol/parsed_data")

lock = threading.Lock()


def get_file_path(snapshot, type, data_dir=DATA_DIR):
	"""
	Gets a snapshot and returns file paths for the parsed color/depth image (depending on type).
	
	:param snapshot: the snapshot containing the raw data paths
	:type snapshot: json
	:param type: the type of image whose path we need ('color'/'depth')
	:type type: str
	:param data_dir: the root directory of the new file paths, defaults to DATA_DIR
	:type data_dir: str, optional
	:returns: path of the new file
	:rtype: str
	:raises: ValueError
	"""
	json_snap = json.loads(snapshot)
	datetime_obj = datetime.fromtimestamp(json_snap['datetime'] / 1000)
	formatted_time = datetime.strftime( datetime_obj, "%Y-%m-%d_%H-%M-%S-%f")
	
	with lock:
		subdir_pathname = os.path.join(data_dir , formatted_time)
		subdir_path = pathlib.Path(subdir_pathname)
		if not subdir_path.is_dir():
			subdir_path.mkdir(parents=True, exist_ok=True)
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
	"""
	Gets a dictionary with snapshot data and returns a
	dictionary containing only data about the user.

	:param json_snap: the json containing the snapshot data
	:type json_snap: json
	:returns: the dictionary containing user data
	:rtype: dict
	"""
	metadata = {
		'user_id' : json_snap['user_id'],
		'username' : json_snap['username'],
		'birthday' : json_snap['birthday'],
		'gender' : json_snap['gender'],
		'datetime' : json_snap['datetime']
	}
	return metadata