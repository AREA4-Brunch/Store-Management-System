"""
    example of using `user_management_db_drop_upgrade_populate` command
        python manage.py user_management_db_drop_upgrade_populate

"""

from app.app import create_app
from flask.cli import FlaskGroup



def main():
    cli = FlaskGroup(create_app=create_app)
    cli()


if __name__ == '__main__':
    main()
