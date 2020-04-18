from . import server as srv
import furl
import click
from  ..message_queue import create_server_publisher
@click.group()
def cli():
	pass

@cli.command('run-server')
@click.option('--host', '-h', default='127.0.0.1')
@click.option('--port', '-p', default=8000)
@click.argument('url')
def run_server(host, port, url):
	publish = parse_url(url)
	return srv.run_server(host, int(port), publish)

# Here you can add other message queue options.
mq_options = {'rabbitmq': create_server_publisher}

def parse_url(url):
	'''
	Receives a url that specifies which message queue we should connect to,
	connects to it and returns a publishing function that the server can use.
	'''
	parsed_url = furl.furl(url)
	for option in mq_options:
		if parsed_url.scheme == option:
			func = mq_options[option]
			return func(parsed_url.host, parsed_url.port)
	else:
		raise ValueError(f"No driver for message queue type {parsed_url.scheme}")

def main(argv):
	print("main is running")
	no_errors = True
	try:
		cli()
	except Exception:
		no_errors = False
		raise
	finally:
		if no_errors:
			print('done')


if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))
