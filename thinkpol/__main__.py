import click
#from . import client as cln
from . import server as srv
from . import web as wb
from .utils import reader as rdr
import pathlib


_DATA_DIR = pathlib.Path(__file__).absolute().parent.parent / 'data'


@click.group()
def cli():
    pass


@click.group()
def server():
    pass


@server.command('run')
@click.argument('address')
def run(address):
    return srv.run_server(address, _DATA_DIR)


cli.add_command(server)

'''
@click.group()
def client():
    pass


@client.command('run')
@click.argument('file_name')
@click.argument('address')
def run(file_name, address):
    return cln.upload_snapshots(file_name, address)


cli.add_command(client)
'''

@cli.command('run_webserver')
@click.argument('address')
@click.argument('data_dir')
def run_webserver(address, data_dir):
    return wb.run_webserver(address, data_dir)


@cli.command('read')
@click.argument('file_name')
def read(file_name):
    r = rdr.Reader(file_name)
    print(r)
    for snapshot in r:
        print(snapshot)


'''

@cli.command('upload_thought')
@click.argument('address')
@click.argument('user')
@click.argument('thought')
def upload_thought(address, user, thought):
    return client.upload_thought(address, user, thought)


@cli.command('run_server')
@click.argument('address')
@click.argument('data')
def run_server(address, data):
    return server.run_server(address, data)
'''


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
