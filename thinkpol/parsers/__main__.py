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
    print(consume(parsers[field]))	# print is temporary, should be redirected to saver

@cli.command('parse')
@click.argument('field')
@click.argument('file_name')
def cli_command_parse(field, file_name):
	with open(file_name, 'r') as f:
		data = f.read()
	return parse(field, data)

def parse_url(url):
	'''
	Receives a url that specifies which message queue we should connect to,
	connects to it and returns a consuming function we can use.
	'''
	parsed_url = furl.furl(url)
	if parsed_url.scheme == 'rabbitmq':
		return create_parser_consumer(parsed_url.host, parsed_url.port)
	# Here you can add other message queue options.
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
