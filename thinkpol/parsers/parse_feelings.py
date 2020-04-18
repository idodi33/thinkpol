import json
from .parser_utils import extract_metadata


def parse_feelings(snapshot):
	js = json.loads(snapshot)
	json_parsed = extract_metadata(js)
	json_parsed['hunger'] = js['hunger']
	json_parsed['thirst'] = js['thirst']
	json_parsed['exhaustion'] = js['exhaustion']
	json_parsed['happiness'] = js['happiness']
	json_parsed = json.dumps(json_parsed)
	return json_parsed

parse_feelings.field = 'feelings'
