import furl
from thinkpol.mdb_driver import mdb_driver as mdb


class Saver:
	def __init__(self, url):
		self.database = parse_url(url)

	def save(self, field, data):
		self.database.save(field, data)


# Here you can add other database options.
db_options = {'mongodb': mdb.DataBase}


def parse_url(url):
	"""
	Receives a url that specifies which database we should connect to,
	connects to it and returns a database object that the server can use.

	:param url: the url we connect to, formatted data_base_type://host:port
	:type url: str
	:returns: the database object
	:rtype: DataBase
	:raises: ValueError
	"""
	parsed_url = furl.furl(url)
	if parsed_url.scheme in db_options:
		init = db_options[parsed_url.scheme]
		host = parsed_url.host or None
		port = parsed_url.port or None
		return init(host, port)
	else:
		raise ValueError(f"No driver for database type {parsed_url.scheme}")