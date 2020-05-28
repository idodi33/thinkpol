import click
import furl
from thinkpol.saver.saver import Saver
from thinkpol.message_queue.rabbitmq_driver import create_saver_consumer
from thinkpol.parsers import parsers


@click.group()
def cli():
    pass


@cli.command('run-saver')
@click.argument('db_url')
@click.argument('mq_url')
def run_saver(db_url, mq_url):
    s = Saver(db_url)
    consume = parse_mq_url(mq_url)
    fields = parsers.keys()
    consume(fields, s)


@cli.command('save')
@click.option('-d', '--database', default='mongodb://')
@click.argument('field')
@click.argument('file_name')
def cli_command_save(database, field, file_name):
	with open(file_name, 'r') as f:
		data = f.read()
	s = Saver(database)
	return s.save(field, data)


# Here you can add other message queue options
mq_options = {'rabbitmq': create_saver_consumer}


def parse_mq_url(url):
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
