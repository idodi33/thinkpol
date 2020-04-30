from datetime import datetime
from PIL import Image
from .parser_utils import get_file_path
from .parser_utils import extract_metadata
import json
import pathlib


def parse_color_image(snapshot, data_dir=None):
	"""
	[description]
	:param snapshot: [description]
	:type snapshot: [type]
	:returns: [description]
	:rtype: {[type]}
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