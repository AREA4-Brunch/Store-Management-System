import logging
from flask_app_extended.config import (
    CustomConfigBase,
    CustomConfigDecoratorBase,
    DefaultConfigFactory,
)
from flask_app_extended.utils.config_utils import (
    DefaultFlaskAppLoggerConfig,
    DefaultURLBlueprintsConfig,
)
from .__secrets import STORE_MANAGEMENT_DB  # in production to replace with env variables



# ========================================================
# Core Configurations Helpers:



class FlaskAppConfig(CustomConfigBase):
    LOGGING_LEVEL = logging.DEBUG

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:{STORE_MANAGEMENT_DB['pwd']}@localhost/store_management"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = "JWT_SECRET_DEV_KEY"
    # JWT_TOKEN_LOCATION = [ 'headers' ]
    # JWT_HEADER_NAME = 'Authorization'
    # JWT_HEADER_TYPE = 'Bearer'
    # JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)
    # JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)



# ========================================================
# Gateways Configuration Helpers:



class RedisAuthorizationConfig(CustomConfigBase):
    HOST = '127.0.0.1'
    PORT = 6379
    DB = 0
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
        DefaultFlaskAppLoggerConfig,
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
