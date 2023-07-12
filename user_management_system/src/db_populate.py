from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .models import Role


def populate(app: Flask, db: SQLAlchemy):
    def populate_roles():
        # populate what does not already exist:
        with app.app_context():
            # data to insert into the db
            roles = [ "owner", "customer", "courier" ]

            for role_name in roles:
                role = Role.query.filter_by(name=role_name).first()
                if role is None: db.session.add(Role(name=role_name))

            db.session.commit()

    populate_roles()
