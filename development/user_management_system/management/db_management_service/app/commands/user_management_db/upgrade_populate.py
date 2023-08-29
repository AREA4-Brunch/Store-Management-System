import click
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from ...scripts import (
    populate,
    update_db_structure,
    create_db_if_not_exists
)


@click.command('user_management_db_upgrade_and_populate')
def user_management_db_upgrade_and_populate():
    db: SQLAlchemy = current_app.container \
                    .services.db_user_management()

    with current_app.app_context() as context:
        create_db_if_not_exists(
            current_app.config['SQLALCHEMY_DATABASE_URI'],
            db
        )

        update_db_structure()
        populate(db)
