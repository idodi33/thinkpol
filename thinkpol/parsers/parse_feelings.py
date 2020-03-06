import json
from .parser_utils import extract_user_metadata


def parse_feelings(snapshot):
	json_snap = json.loads(snapshot)
	json_parsed = extract_user_metadata(json_snap)
	json_parsed['hunger'] = json_snap['hunger']
	json_parsed['thirst'] = json_snap['thirst']
	json_parsed['exhaustion'] = json_snap['exhaustion']
	json_parsed['happiness'] = json_snap['happiness']
	json_parsed = json.dumps(json_parsed)
	return json_parsed

parse_feelings.field = 'feelings'
