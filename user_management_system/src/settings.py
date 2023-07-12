import logging
from datetime import timedelta

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



# optional app's name
APP_NAME = None

DEBUG = True

LOGGING_HANDLER = logging.FileHandler('./logs/log1.log')
LOGGING_HANDLER.setLevel(logging.DEBUG)

DATABASES = {
    "users": {
        "database": SQLAlchemy(),
        "migrate": Migrate(),
        # (module_name, function_name)
        "populate": ('src.db_populate', 'populate')
    }
}

class FLASK_APP_CONFIGURATION:
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/authentication'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = "YOU'LL NEVER GUESS ME"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
