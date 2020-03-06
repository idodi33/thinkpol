from datetime import datetime
from PIL import Image
from .parser_utils import get_file_path
from .parser_utils import extract_user_metadata
import json
import pathlib


def parse_color_image(snapshot):
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
	json_parsed = extract_user_metadata(json_snap)
	json_parsed['color_image'] = str(color_file_path)
	json_parsed = json.dumps(json_parsed)	# turns our dictionary into something we can send forward.
	return json_parsed

parse_color_image.field = "color_image"