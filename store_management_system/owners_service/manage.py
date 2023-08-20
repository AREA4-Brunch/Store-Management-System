"""
    example of starting the app
        python manage.py run --host=localhost --port=5001 --debug

"""

from app.app import create_app
from flask.cli import FlaskGroup



def main():
    cli = FlaskGroup(create_app=create_app)
    cli()


if __name__ == '__main__':
    main()
