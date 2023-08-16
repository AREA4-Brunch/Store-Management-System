from app.app import IoCAppContainer, get_app
from flask.cli import FlaskGroup


def main():
    container = IoCAppContainer()
    # must be done here:
    container.init_resources()
    container.wire(modules=[ 'app.app', ])

    # to start app
    # python manage.py run --host=localhost --port=5000 --debug
    cli = FlaskGroup(create_app=get_app)
    cli()


if __name__ == '__main__':
    main()
