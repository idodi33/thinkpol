from .api import API
import furl
from ..mdb_driver import mdb_driver as mdb

def run_api_server(host, port, database_url):
	database = parse_url(database_url)
	API(host, port, database)
	API.api.run(host=host, port=port)

# Here you can add other database options.
db_options = {'mongodb': mdb.DataBase}

def parse_url(url):
	'''
	Receives a url that specifies which database we should connect to,
	connects to it and returns a database object that the server can use.
	'''
	parsed_url = furl.furl(url)
	for option in db_options:
		if parsed_url.scheme == option:
			host = parsed_url.host or None
			port = parsed_url.port or None
			return db_options[option](host, port)
	else:
		raise ValueError(f"No driver for database type {parsed_url.scheme}")