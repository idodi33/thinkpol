from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from .parser_utils import get_file_path
from .parser_utils import extract_user_metadata
import json
import pathlib


def parse_depth_image(snapshot):
	json_snap = json.loads(snapshot)
	depth_file_path = get_file_path(snapshot, 'depth')		# path of the file that will contain the parsed image
	raw_file_path_name = json_snap['depth_image']	# path of the file that contains the raw data
	raw_file_path = pathlib.Path(raw_file_path_name)
	data = np.fromfile(raw_file_path, dtype=np.float32)
	print(f"Size of data array is {len(data)}")
	width = json_snap['d_width']
	height = json_snap['d_height']
	data_matrix = np.reshape(data, (height, width))
	plt.imshow(data_matrix, cmap='hot', interpolation='nearest')
	print(f"Depth file path is {depth_file_path}")
	plt.savefig(depth_file_path)
	json_parsed = extract_user_metadata(json_snap)
	json_parsed['depth_image'] = str(depth_file_path)
	json_parsed = json.dumps(json_parsed)	# turns our dictionary into something we can send forward.
	return json_parsed

parse_depth_image.field = "depth_image"