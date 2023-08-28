import click
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import (
    database_exists, create_database, drop_database
)
from flask_migrate import init, migrate, upgrade



@click.command('store_management_db_drop_upgrade_populate')
def store_management_db_drop_upgrade_populate():
    db: SQLAlchemy = current_app.container \
                    .services.db_store_management()

    uri = current_app.config['SQLALCHEMY_DATABASE_URI']

    def create_db_if_not_exists(uri):
        if not database_exists(uri):
            create_database(uri)
        db.create_all()

    def update_db_structure():
        migrate(message='Production Migration; store_management_db_drop_upgrade_populate')
        upgrade()

    with current_app.app_context() as context:
        # if already non existant just return
        if not database_exists(uri):
            return

        # drop the entire database
        drop_database(uri)

        create_db_if_not_exists(uri)
        update_db_structure()
