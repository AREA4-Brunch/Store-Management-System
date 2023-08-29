from flask_sqlalchemy import SQLAlchemy
from ..models import User, Role, HasRole



def populate(db: SQLAlchemy):
    def populate_roles():
        # populate what does not already exist:
        # with app.app_context():
        # data to insert into the db
        roles = [ "owner", "customer", "courier" ]

        for role_name in roles:
            role = Role.query.filter_by(name=role_name).first()
            if role is None: db.session.add(Role(name=role_name))

        db.session.commit()

    def add_users():
        owners = [
            User(
                email="onlymoney@gmail.com",
                forename='Scrooge',
                surname='McDuck',
                password='evenmoremoney'
            )
        ]

        owner_role = Role.query.filter_by(name='owner').first()
        if owner_role is None:
            raise Exception('Tried to add owner but no role `owner` exists.')

        for owner in owners:
            if not User.query.filter_by(email=owner.email).first():
                db.session.add(owner)
                db.session.flush()
                has_role = HasRole(user_id=owner.id,
                                   role_id=owner_role.id)
                db.session.add(has_role)

        db.session.commit()

    # with app.app.app_context() as _:
    populate_roles()
    add_users()
