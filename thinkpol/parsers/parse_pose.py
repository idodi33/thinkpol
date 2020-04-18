import json
from .parser_utils import extract_metadata


def parse_pose(snapshot):
	js = json.loads(snapshot)
	json_parsed = extract_metadata(js)
	(x, y, z) = js['translation']
	json_parsed['translation_x'] = x
	json_parsed['translation_y'] = y
	json_parsed['translation_z'] = z
	(x, y, z, w) = js['rotation']
	json_parsed['rotation_x'] = x
	json_parsed['rotation_y'] = y
	json_parsed['rotation_z'] = z
	json_parsed['rotation_w'] = w
	json_parsed = json.dumps(json_parsed)
	return json_parsed

parse_pose.field = 'pose'