import click
from . import client
from . import server
from . import web


@click.group()
def cli():
    pass


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


@cli.command('run_webserver')
@click.argument('address')
@click.argument('data_dir')
def run_webserver(address, data_dir):
    return web.run_webserver(address, data_dir)


def main(argv):
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
