import logging
from datetime import timedelta

from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate



class Settings:
    # optional app's name
    APP_NAME = None
    HOST = '127.0.0.1'
    PORT = 5000

    DEBUG = True

    LOGGER_LEVEL = logging.DEBUG
    LOGGING_HANDLER = logging.FileHandler('./logs/log1.log')
    LOGGING_HANDLER.setLevel(LOGGER_LEVEL)
    LOGGING_HANDLER.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )

    DATABASES = {
        "users": {
            "uri": 'mysql+pymysql://root:gN?*ec2dwiw3?(Cyfhel@localhost/authentication',
            "database": SQLAlchemy(),
            # "migrate": Migrate(),
            # (module_name, function_name)
            "init": ('src.init', 'db_init'),
        }
    }

    ON_INIT = (
        {  # Redis
            'init': ('src.init', 'redis_init'),
            'host': '127.0.0.1',
            'port': 6379,
            'db': 0,
            'decode_responses': True
        },
        {  # JWT
            'init': ('src.init', 'jwt_init'),
        },
    )


class FLASK_APP_CONFIGURATION:
    LOGGING_LEVEL = Settings.LOGGER_LEVEL

    SQLALCHEMY_DATABASE_URI = Settings.DATABASES["users"]["uri"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = "JWT_SECRET_DEV_KEY"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
