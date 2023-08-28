import redis

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from sqlalchemy_utils import database_exists, create_database

from .apps import App
from .models import Role, User, HasRole
from .utils import get_expiry_hour


def db_init(app: App, db_config: dict):
    db: SQLAlchemy = db_config['database']

    def create_if_not_exists():
        if not database_exists(db_config['uri']):
            create_database(db_config['uri'])
        db.create_all()

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
    create_if_not_exists()
    populate_roles()
    add_users()


def redis_init(app: App, config):
    redis_client = redis.StrictRedis(
        host=config['host'],
        port=config['port'],
        db=config['db'],
        decode_responses=config['decode_responses']
    )
    app['redis_client'] = redis_client


def jwt_init(app: App, config):
    jwt = JWTManager(app.app)
    app['jwt'] = jwt

    # add redis blocklist checker to jwt_required feature
    @jwt.token_in_blocklist_loader
    def is_jwt_in_blocklist(jwt_header: dict, jwt_payload: dict) -> bool:
        jti = jwt_payload['jti']
        expiry_hour, time_format = get_expiry_hour(jwt_payload)
        blocklist_group = f'jwt_blk:exp={expiry_hour}'
        return app['redis_client'].sismember(blocklist_group, jti)
