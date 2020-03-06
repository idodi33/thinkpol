import click
from . import client as cln

@click.group()
def cli():
    pass

@cli.command('upload-sample')
@click.option('--host', '-h', default='127.0.0.1')
@click.option('--port', '-p', default=8000)
@click.argument('path')
def upload(host, port, path):
    return cln.upload_sample(host, int(port), path)


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
