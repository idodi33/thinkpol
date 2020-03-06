import pathlib
import importlib
import os
import sys

# This framework collects functions that start with 'parse_' and adds them to the parsers dict.
parsers = dict()
root = pathlib.Path.cwd() /'thinkpol/parsers/'
sys.path.insert(0, str(root.parent))
for path in root.iterdir():
	if path.name.startswith("_") or not path.suffix == '.py':
		continue
	module = (importlib.import_module(f'{root.name}.{path.stem}', package=root.name))
	for name, item in module.__dict__.items():
		if callable(item) and name.startswith("parse_"):
			parsers[item.field] = item

def parse(field, data):
	'''
	Parses the data with the parser that corresponds to field.
	'''
	if not parsers[field]:
		raise ValueError(f"No parser for field {field}.")
	return parsers[field](data)
