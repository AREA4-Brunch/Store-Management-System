from flask_sqlalchemy import SQLAlchemy
# from .app import get_app


# db: SQLAlchemy = get_app().container.services.db_store_management()
# MIGRATE: SQLAlchemy = get_app().container.services.migrate_db_store_management()


# ====================================================
# Exceptions:



class InvalidPassword(Exception):
    pass



# ====================================================
# Database Models:



def create_models(db: SQLAlchemy) -> dict:
    class HasRole(db.Model):
        __tablename__ = "has_role"

        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
        role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)

        def __repr__(self) -> str:
            return f'<HasRole(id: {self.id}): User {self.user_id} has role: {self.role_id}>'


    class User(db.Model):
        __tablename__ = "users"

        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(256), nullable=False, unique=True)
        forename = db.Column(db.String(256), nullable=False)
        surname = db.Column(db.String(256), nullable=False)
        # not stored as salty hash
        password = db.Column(db.String(256), nullable=False)

        roles = db.relationship(
            "Role",
            secondary=HasRole.__table__,
            back_populates="users"  # Role.users
        )

        def __init__(self, email, forename, surname, password):
            self.email = email
            self.forename = forename
            self.surname = surname
            self.set_password(password)

        def __repr__(self):
            return f'<User(id: {self.id}): {self.forename} {self.surname}; pwd: {self.password}, email: {self.email}>'

        def set_password(self, password):
            # self.password = generate_password_hash(password)

            def validate():
                if len(password) < 8:
                    raise InvalidPassword()

            validate()
            self.password = password

        def check_password(self, password):
            # return check_password_hash(self.password, password)
            return self.password == password

        def delete(self):
            # remove all has_role objects that have user.id as foreign key
            db.session.query(HasRole).with_for_update() \
                    .filter(HasRole.user_id == self.id).delete()
            db.session.delete(self)


    class Role(db.Model):
        __tablename__ = "roles"

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(64), nullable=False, unique=True)

        users = db.relationship(
            "User",
            secondary=HasRole.__table__,
            back_populates="roles"  # User.roles
        )

        def __repr__(self) -> str:
            return f'<Role(id: {self.id}): {self.name}>'


    # add all classes that should be returned and group them
    # in dictionary by their own name
    classes = [
        HasRole,
        User,
        Role,
    ]

    # return each class under its own name in dict
    classes_dict = dict()

    for class_ in classes:
        classes_dict[class_.__name__] = class_

    return classes_dict
