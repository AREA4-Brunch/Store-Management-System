"""
    example of using `store_management_db_upgrade_and_populate` command
        python manage.py store_management_db_upgrade_and_populate

"""

from app.app import create_app
from flask.cli import FlaskGroup



def main():
    cli = FlaskGroup(create_app=create_app)
    cli()


if __name__ == '__main__':
    main()
