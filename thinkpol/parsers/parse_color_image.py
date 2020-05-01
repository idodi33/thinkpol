from datetime import datetime
from PIL import Image
from parsers.parser_utils import get_file_path
from parsers.parser_utils import extract_metadata
import json
import pathlib


def parse_color_image(snapshot, data_dir=None):
	"""
	Gets a snapshot containing a path to raw color image data, 
	parses that data and saves it in a path depending on the optional
	data_dir argument, and returns information about that snapshot
	in json format.

	:param snapshot: the snapshot we're parsing
	:type snapshot: json
	:param data_dir: the directory in which we want to save the parsed image
	:type data_dir: str, optional
	:returns: a json containing information about the snapshot, including the address
	of the parsed color image we've saved
	:rtype: json
	"""
	js = json.loads(snapshot)
	if data_dir:
		# path of the file that will contain the parsed image
		path = get_file_path(snapshot, 'color', data_dir)
	else:
		path = get_file_path(snapshot, 'color')	
	data = pathlib.Path(js['color_image']).read_bytes()	# raw data we are to parse
	size = js['c_width'], js['c_height']
	image = Image.frombytes('RGB', size, data)
	image.save(path)
	json_parsed = extract_metadata(js)
	json_parsed['color_image'] = str(path)
	json_parsed = json.dumps(json_parsed)	# turns our dictionary into something we can send forward.
	return json_parsed


parse_color_image.field = "color_image"