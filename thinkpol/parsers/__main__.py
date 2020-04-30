import click
import furl
from . import parsers, parse
from ..message_queue.rabbitmq_driver import create_parser_consumer
#from ..message_queue.rabbitmq_driver import parser_publish


@click.group()
def cli():
    pass


@cli.command('run-parser')
@click.argument('field')
@click.argument('url')
def run_parser(field, url):
    consume = parse_url(url)
    consume(parsers[field])	# print is temporary, should be redirected to saver


@cli.command('parse')
@click.argument('field')
@click.argument('file_name')
def cli_command_parse(field, file_name):
	with open(file_name, 'r') as f:
		data = f.read()
	return parse(field, data)


# Here you can add other message queue options.
mq_options = {'rabbitmq': create_parser_consumer}


def parse_url(url):
	'''
	Receives a url that specifies which message queue we should connect to,
	connects to it and returns a consuming function we can use.
	'''
	parsed_url = furl.furl(url)
	if parsed_url.scheme in mq_options:
		func = mq_options[parsed_url.scheme]
		return func(parsed_url.host, parsed_url.port)
	else:
		raise ValueError(f"No driver for message queue type {parsed_url.scheme}")


def main(argv):
	print("main is running")
	cli()
	print('done')


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
