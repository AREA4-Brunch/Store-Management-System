import click
from ... import APP



@APP.cli.command('runserver')
@click.argument('host', type=str, required=False, default='127.0.0.1')
@click.argument('port', type=int, required=False, default=5000)
def runserver(host, port):
    APP.run(host=host, port=port)  # [noreturn]
