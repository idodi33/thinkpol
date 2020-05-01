"""
Creates an API server that presents data as pulled from a database.
:param db_options: a dictionary containing options for database objects
from which we can pull data
:type db_options: dict
"""

from .api import API
import furl
from thinkpol.mdb_driver import mdb_driver as mdb


def run_api_server(host, port, database_url):
	"""
	Runs an API server that connects to a specified database
	and presents data from there.

	:param host: the api connection's host
	:type host: str
	:param port: the api connection's port
	:type port: int
	:param database_url: a formatted url specifying the database we connect to
	:type database_url: str
	"""
	database = parse_url(database_url)
	API(host, port, database)
	API.api.run(host=host, port=port)


# Here you can add other database options.
db_options = {'mongodb': mdb.DataBase}


def parse_url(url):
	"""
	Receives a url that specifies which database we should connect to,
	connects to it and returns a database object that the server can use.

	:param url: the database format url (formatted database_type://host:port)
	:type url: str
	:returns: a corresponding database object
	:rtype: DataBase
	:raises: ValueError
	"""
	parsed_url = furl.furl(url)
	if parsed_url.scheme in db_options:
		host = parsed_url.host or None
		port = parsed_url.port or None
		return db_options[parsed_url.scheme](host, port)
	else:
		raise ValueError(f"No driver for database type {parsed_url.scheme}")