import click
import furl
from . import run_api_server


@click.group()
def cli():
    pass

@cli.command('run-server')
@click.option('--host', '-h', default='127.0.0.1')
@click.option('--port', '-p', default=5000)
@click.option('--database', '-d', default='mongodb://')
def run_server(host, port, database):
    run_api_server(host, port, database)

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
