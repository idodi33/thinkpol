"""
A framework that collects classes that end with 'Driver' 
and adds them to the drivers dict.
"""
import inspect
import sys
import os
import pathlib
import importlib

"""
This framework collects classes that end with 'Driver' 
and adds them to the drivers dict.
"""
drivers = dict()
root = pathlib.Path(os.path.dirname(__file__))
sys.path.insert(0, str(root.parent))
for path in root.iterdir():
	if path.name.startswith("_") or not path.suffix == '.py':
		continue
	module = (importlib.import_module(
		f'{root.name}.{path.stem}', package=root.name
		))
	for name, item in module.__dict__.items():
		if inspect.isclass(item) and name.endswith("Driver"):
			drivers[item.field] = item