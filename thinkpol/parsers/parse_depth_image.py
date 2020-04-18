from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from .parser_utils import get_file_path
from .parser_utils import extract_metadata
import json
import pathlib


def parse_depth_image(snapshot):
	js = json.loads(snapshot)
	depth_file_path = get_file_path(snapshot, 'depth')  # path of the file that will contain the parsed image	
	raw_file_path = pathlib.Path(js['depth_image'])		# path of the file that contains the raw data
	data = np.fromfile(raw_file_path, dtype=np.float32)
	print(f"Size of data array is {len(data)}")
	size =js['d_height'], js['d_width']
	data_matrix = np.reshape(data, size)
	plt.imshow(
		data_matrix, 
		cmap='hot', 
		interpolation='nearest'
		)
	print(f"Depth file path is {depth_file_path}")
	plt.savefig(depth_file_path)
	json_parsed = extract_metadata(js)
	json_parsed['depth_image'] = str(depth_file_path)
	json_parsed = json.dumps(json_parsed)	# turns our dictionary into something we can send forward.
	return json_parsed

parse_depth_image.field = "depth_image"