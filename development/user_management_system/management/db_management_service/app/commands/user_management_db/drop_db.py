import click
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, drop_database



@click.command('user_management_db_drop_db')
def user_management_db_drop_db():
    db: SQLAlchemy = current_app.container \
                    .services.db_user_management()
    uri = current_app.config['SQLALCHEMY_DATABASE_URI']

    with current_app.app_context() as context:
        # if already non existant just return
        if not database_exists(uri):
            return

        # drop the entire database
        drop_database(uri)
