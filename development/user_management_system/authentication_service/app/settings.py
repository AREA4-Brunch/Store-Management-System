import logging
import os
from datetime import timedelta
from flask_app_extended.config import (
    CustomConfigBase,
    CustomConfigDecoratorBase,
    DefaultConfigFactory,
)
from flask_app_extended.utils.config_utils import (
    DefaultFlaskAppLoggerConfig,
    DefaultURLBlueprintsConfig,
)
from .__secrets import USER_MANAGEMENT_DB  # in production to replace with env variables


DB_USER_MANAGEMENT_URI = os.environ.get(
    'DB_USER_MANAGEMENT_URI',
    f"mysql+pymysql://root:{USER_MANAGEMENT_DB['pwd']}@localhost/authentication"
)
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'JWT_SECRET_DEV_KEY')
REDIS_BLOCKLIST_HOST = os.environ.get('REDIS_BLOCKLIST_HOST', '127.0.0.1')
REDIS_BLOCKLIST_PORT = int(os.environ.get('REDIS_BLOCKLIST_PORT', 6379))
REDIS_BLOCKLIST_DB = int(os.environ.get('REDIS_BLOCKLIST_DB', 0))
PATH_LOGGING_DIR = os.environ.get('PATH_LOGGING_DIR', './logs/')
LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', 'DEBUG')



# ========================================================
# Core Configurations Helpers:



class FlaskAppConfig(CustomConfigBase):
    LOGGING_LEVEL = getattr(logging, LOGGING_LEVEL)

    SQLALCHEMY_DATABASE_URI = DB_USER_MANAGEMENT_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = JWT_SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    # JWT_TOKEN_LOCATION = [ 'headers' ]
    # JWT_HEADER_NAME = 'Authorization'
    # JWT_HEADER_TYPE = 'Bearer'


class FileLoggerConfig(DefaultFlaskAppLoggerConfig):
    LOG_FILE_PATH = os.path.join(PATH_LOGGING_DIR, 'log1.log')



# ========================================================
# Gateways Configuration Helpers:



class RedisAuthorizationConfig(CustomConfigBase):
    HOST = REDIS_BLOCKLIST_HOST
    PORT = REDIS_BLOCKLIST_PORT
    DB = REDIS_BLOCKLIST_DB
    DECODE_RESPONSES = True


class RedisGatewaysConfiguration(CustomConfigDecoratorBase):
    auth = RedisAuthorizationConfig()



# ========================================================
# App Configuration:



class CoreConfiguration(CustomConfigDecoratorBase):
    flask_app = FlaskAppConfig()

    # flask_app_extended lib's settings assume in
    # app_utils.DefaultAppInitializer
    flask_app_extended = DefaultConfigFactory(flask_app, [
        FileLoggerConfig,
        DefaultURLBlueprintsConfig,
    ]).create_config()


class GatewaysConfiguration(CustomConfigDecoratorBase):
    redis = DefaultConfigFactory(CustomConfigBase(), [
        RedisGatewaysConfiguration,
    ]).create_config()


class AppConfiguration(CustomConfigBase):
    core = DefaultConfigFactory(CustomConfigBase(), [
        CoreConfiguration,
    ]).create_config()

    gateways = DefaultConfigFactory(CustomConfigBase(), [
        GatewaysConfiguration,
    ]).create_config()
