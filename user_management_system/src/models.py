from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash


from .settings import DATABASES


# ====================================================
# Globals:



DATABASE: SQLAlchemy = DATABASES["users"]["database"]
MIGRATE: Migrate = DATABASES["users"]["migrate"]



# ====================================================
# Exceptions:



class InvalidPassword(Exception):
    pass



# ====================================================
# Database Models:



class HasRole(DATABASE.Model):
    __tablename__ = "has_role"

    id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    user_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey("users.id"), nullable=False)
    role_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey("roles.id"), nullable=False)

    def __repr__(self) -> str:
        return f'<HasRole(id: {self.id}): User {self.user_id} has role: {self.role_id}>'



class User(DATABASE.Model):
    __tablename__ = "users"

    id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    email = DATABASE.Column(DATABASE.String(256), nullable=False, unique=True)
    forename = DATABASE.Column(DATABASE.String(256), nullable=False)
    surname = DATABASE.Column(DATABASE.String(256), nullable=False)
    # not stored as salty hash
    password = DATABASE.Column(DATABASE.String(256), nullable=False)

    roles = DATABASE.relationship(
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
        return check_password_hash(self.password, password)

    def delete(self):
        # remove all has_role objects that have user.id as foreign key
        DATABASE.session.query(HasRole).with_for_update() \
                .filter(HasRole.user_id == self.id).delete()
        DATABASE.session.delete(self)



class Role(DATABASE.Model):
    __tablename__ = "roles"

    id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    name = DATABASE.Column(DATABASE.String(64), nullable=False, unique=True)

    users = DATABASE.relationship(
        "User",
        secondary=HasRole.__table__,
        back_populates="roles"  # User.roles
    )

    def __repr__(self) -> str:
        return f'<Role(id: {self.id}): {self.name}>'


if __name__ == "__main__":
    pass
