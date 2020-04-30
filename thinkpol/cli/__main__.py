import requests
import click
import furl
import pathlib
import json


@click.group()
def cli():
    pass

@cli.command('get-users')
@click.option('-h', '--host', default='127.0.0.1')
@click.option('-p', '--port', default='5000')
def get_users(host, port):
    url = furl.furl("http://")
    url.set(host=host, port=port, path=['users'])
    r = requests.get(url.url)
    print(r.json())

@cli.command('get-user')
@click.option('-h', '--host', default='127.0.0.1')
@click.option('-p', '--port', default='5000')
@click.argument('user_id')
def get_user(host, port, user_id):
    url = furl.furl("http://")
    url.set(host=host, port=port, path=['users', user_id])
    r = requests.get(url.url)
    print(r.json())

@cli.command('get-snapshots')
@click.option('-h', '--host', default='127.0.0.1')
@click.option('-p', '--port', default='5000')
@click.argument('user_id')
def get_snapshots(host, port, user_id):
    url = furl.furl("http://")
    url.set(host=host, port=port, path=['users', user_id, 'snapshots'])
    r = requests.get(url.url)
    print(r.json())

@cli.command('get-snapshot')
@click.option('-h', '--host', default='127.0.0.1')
@click.option('-p', '--port', default='5000')
@click.argument('user_id')
@click.argument('snapshot_id')
def get_snapshot(host, port, user_id, snapshot_id):
    url = furl.furl("http://")
    url.set(host=host, port=port, path=['users', user_id, 
    'snapshots', snapshot_id])
    r = requests.get(url.url)
    print(r.json())

@cli.command('get-result')
@click.option('-h', '--host', default='127.0.0.1')
@click.option('-p', '--port', default='5000')
@click.option('-s', '--save', default=None)
@click.argument('user_id')
@click.argument('snapshot_id')
@click.argument('result_name')
def get_result(host, port, save, user_id, snapshot_id, result_name):
    url = furl.furl("http://")
    url.set(host=host, port=port, path=['users', user_id, 
    'snapshots', snapshot_id, result_name])
    r = requests.get(url.url)
    if save:
    	path = pathlib.Path(save)
    	print(f'parent is {path.parent}')
    	if not path.parent.is_dir():	# If this file doesn't exist, create it
    		path.parent.mkdir(parents=True)
    	if not path.is_file():
    		path.touch()
    	with open(save, 'w') as f:
    		f.write(json.dumps(*r.json()))
    print(r.json())


def main(argv):
	print("main is running")
	cli()
	print('done')


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
