import struct
from datetime import datetime
from thinkpol.reader.reader_drivers import drivers

_USR_FORMAT = "user {0}: {1}, born {2} ({3})"


class Reader:
	"""
	Reads information (about users and their snapshots) from a formatted binary file.
	A Reader object can be used as an iterable, going through all its snapshots.

	:param file_name: name of the file
	:type file_name: str
	:param format: format of the file ('binary' or 'protobuf')
	:type format: str
	"""

	def __init__(self, file_name, format):
		self.format = format
		if format in drivers:
			driver = drivers[format](file_name)
		else:
			raise ValueError(f'Invalid format: {format}')
		self.user_id, self.user_name, self.birth_date, \
		self.gender, = driver.get_user_info()
		self.snapshots_iterator = driver.get_snap_iterator()

	def __str__(self):
		dttime = datetime.fromtimestamp(self.birth_date)
		fmt_date = dttime.strftime("%B %d, %Y")
		data = _USR_FORMAT.format(
			self.user_id, self.user_name,
			fmt_date, self.gender
			)
		return data

	def __iter__(self):
		return iter(self.snapshots_iterator)

