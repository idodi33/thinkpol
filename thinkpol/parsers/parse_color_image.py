from datetime import datetime
from PIL import Image
from .parser_utils import get_file_path
from .parser_utils import extract_metadata
import json
import pathlib


'''def parse_color_image(snapshot):
	json_snap = json.loads(snapshot)
	color_file_path = get_file_path(snapshot, 'color')		# path of the file that will contain the parsed image
	raw_file_path_name = json_snap['color_image']	# path of the file that contains the raw data
	raw_file_path = pathlib.Path(raw_file_path_name)
	data = raw_file_path.read_bytes()
	data_len = json_snap['c_width'] * json_snap['c_height'] * 3
	rgb_triplets = [(data[i], data[i + 1], data[i + 2]) for i in range(0, data_len, 3)]
	image = Image.new("RGB", (json_snap['c_width'], json_snap['c_height']))
	image.putdata(rgb_triplets)
	image.save(color_file_path)
	json_parsed = extract_metadata(json_snap)
	json_parsed['color_image'] = str(color_file_path)
	json_parsed = json.dumps(json_parsed)	# turns our dictionary into something we can send forward.
	return json_parsed'''

def parse_color_image(snapshot):
	js = json.loads(snapshot)
	path = get_file_path(snapshot, 'color')		# path of the file that will contain the parsed image
	data = pathlib.Path(js['color_image']).read_bytes()	# raw data we are to parse
	size = js['c_width'], js['c_height']
	image = Image.frombytes('RGB', size, data)
	image.save(path)
	json_parsed = extract_metadata(js)
	json_parsed['color_image'] = str(path)
	json_parsed = json.dumps(json_parsed)	# turns our dictionary into something we can send forward.
	return json_parsed

parse_color_image.field = "color_image"