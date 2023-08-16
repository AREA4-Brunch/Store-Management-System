import click
from flask import Flask


def init(app: Flask):
    @app.cli.command('runserver')
    @click.argument('host', type=str, required=False, default='127.0.0.1')
    @click.argument('port', type=int, required=False, default=5000)
    @click.option('--debug', is_flag=True, default=True)
    def runserver(host, port, debug):
        print('failing here')
        app.run(host=host, port=port, debug=debug)  # [noreturn]
