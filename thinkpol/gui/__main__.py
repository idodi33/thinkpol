import click
from thinkpol.gui import run_gui_server

@click.group()
def cli():
    pass

@cli.command('run-server')
@click.option('-h', '--host', default='127.0.0.1')
@click.option('-p', '--port', default='8080')
@click.option('-H', '--api-host', default='127.0.0.1')
@click.option('-P', '--api-port', default='5000')
def click_run_gui_server(host, port, api_host, api_port):
	print(f"{host}, {port}, {api_host}, {api_port}")
	return run_gui_server(host, port, api_host, api_port)


def main(argv):
	print("main is running")
	cli()
	print('done')


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))