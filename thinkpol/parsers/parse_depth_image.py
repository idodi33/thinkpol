from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from parsers.parser_utils import get_file_path
from parsers.parser_utils import extract_metadata
import json
import pathlib
import os


def parse_depth_image(snapshot, data_dir=None):
	"""
	Gets a snapshot containing a path to raw depth image data, 
	parses that data and saves it in a path depending on the optional
	data_dir argument, and returns information about that snapshot
	in json format.

	:param snapshot: the snapshot we're parsing
	:type snapshot: json
	:param data_dir: the directory in which we want to save the parsed image
	:type data_dir: str, optional
	:returns: a json containing information about the snapshot, including the address
	of the parsed depth image we've saved
	:rtype: json
	"""

	js = json.loads(snapshot)
	if data_dir:
		# path of the file that will contain the parsed image
		depth_file_path = get_file_path(snapshot, 'depth', data_dir)
	else:
		depth_file_path = get_file_path(snapshot, 'depth')	
	raw_file_path = pathlib.Path(js['depth_image'])		# path of the file that contains the raw data
	print(f"parse_depth_image: raw_file_path is {raw_file_path}")
	with open(raw_file_path, "rb") as f:
		f.seek(0, os.SEEK_END)
		print(f"depth file length is {f.tell()}")
	data = np.fromfile(raw_file_path, dtype=np.float32)
	print(f"Size of data array is {len(data)}")
	size =js['d_height'], js['d_width']
	data_matrix = np.reshape(data, size)
	plt.imshow(data_matrix, cmap='hot', interpolation='nearest')
	print(f"Depth file path is {depth_file_path}")
	plt.savefig(depth_file_path)
	json_parsed = extract_metadata(js)
	json_parsed['depth_image'] = str(depth_file_path)
	json_parsed = json.dumps(json_parsed)	# turns our dictionary into something we can send forward.
	return json_parsed


parse_depth_image.field = "depth_image"