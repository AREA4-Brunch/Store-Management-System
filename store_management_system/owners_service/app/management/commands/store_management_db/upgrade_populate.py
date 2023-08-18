import click
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database


@click.command('store_management_db_upgrade_and_populate')
def store_management_db_upgrade_and_populate():
    db: SQLAlchemy = current_app.container \
                    .services.db_store_management()

    def create_db_if_not_exists(uri):
        if not database_exists(uri):
            create_database(uri)
        db.create_all()

    with current_app.app_context() as context:
        create_db_if_not_exists(
            current_app.config['SQLALCHEMY_DATABASE_URI']
        )
