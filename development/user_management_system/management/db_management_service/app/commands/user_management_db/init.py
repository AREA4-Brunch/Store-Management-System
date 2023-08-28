import click
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database
from flask_migrate import init, migrate, upgrade
from ...scripts.populate import populate



@click.command('user_management_db_init')
def user_management_db_init():
    db: SQLAlchemy = current_app.container \
                    .services.db_user_management()

    def create_db_if_not_exists(uri):
        if not database_exists(uri):
            create_database(uri)
        db.create_all()

    def update_db_structure():
        init()
        migrate(message='Initial Production Migration; user_management_db_init')
        upgrade()

    with current_app.app_context() as context:
        create_db_if_not_exists(
            current_app.config['SQLALCHEMY_DATABASE_URI']
        )

        update_db_structure()
        populate(db)

