from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import (
    database_exists, create_database, drop_database
)


def create_db_if_not_exists(uri, db: SQLAlchemy):
    if not database_exists(uri):
        create_database(uri)
    db.create_all()
