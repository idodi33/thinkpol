import json
from .parser_utils import extract_user_metadata


def parse_pose(snapshot):
	json_snap = json.loads(snapshot)
	json_parsed = extract_user_metadata(json_snap)
	json_parsed['translation'] = json_snap['translation']	# this is a 3-tuple
	json_parsed['rotation'] = json_snap['rotation']		# this is a 4-tuple
	json_parsed = json.dumps(json_parsed)
	return json_parsed

parse_pose.field = 'pose'