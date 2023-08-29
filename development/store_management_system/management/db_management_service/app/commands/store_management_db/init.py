import click
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from ...scripts import (
    create_db_if_not_exists,
    update_db_structure
)



@click.command('store_management_db_init')
def store_management_db_init():
    db: SQLAlchemy = current_app.container \
                    .services.db_store_management()
    logger = current_app.logger


    with current_app.app_context() as context:
        create_db_if_not_exists(
            current_app.config['SQLALCHEMY_DATABASE_URI'],
            db
        )

        update_db_structure()

