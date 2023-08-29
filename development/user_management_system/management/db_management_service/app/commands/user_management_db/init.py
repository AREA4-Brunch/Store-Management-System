import click
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from ...scripts import populate, update_db_structure, create_db_if_not_exists



@click.command('user_management_db_init')
def user_management_db_init():
    db: SQLAlchemy = current_app.container \
                    .services.db_user_management()
    # logger = current_app.logger

    with current_app.app_context() as context:
        create_db_if_not_exists(
            current_app.config['SQLALCHEMY_DATABASE_URI'],
            db
        )

        update_db_structure()
        populate(db)
