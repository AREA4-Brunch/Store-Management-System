import logging
from libs.flask_app_extended.config import (
    CustomConfigBase,
    CustomConfigDecoratorBase,
    DefaultConfigFactory,
)



# ========================================================
# Core Configurations Helpers:



from libs.flask_app_extended.utils.config_utils import (
    DefaultFlaskAppLoggerConfig,
    DefaultBlueprintsConfig,
)


class FlaskAppConfig(CustomConfigBase):
    DEBUG = True

    LOGGING_LEVEL = logging.DEBUG

    # SQLALCHEMY_DATABASE_URI = Settings.DATABASES["users"]["uri"]
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = "JWT_SECRET_DEV_KEY"
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
    auth = DefaultConfigFactory(
        RedisAuthorizationConfig
    ).create_config()



# ========================================================
# App Configuration:



class CoreConfiguration(CustomConfigDecoratorBase):
    flask_app = DefaultConfigFactory(FlaskAppConfig, [
        DefaultFlaskAppLoggerConfig,
        DefaultBlueprintsConfig,
    ]).create_config()


class GatewaysConfiguration(CustomConfigDecoratorBase):
    redis = DefaultConfigFactory(CustomConfigBase, [
        RedisGatewaysConfiguration,
    ]).create_config()


class AppConfiguration(CustomConfigBase):
    core = DefaultConfigFactory(CustomConfigBase, [
        CoreConfiguration,
    ]).create_config()

    gateways = DefaultConfigFactory(CustomConfigBase, [
        GatewaysConfiguration,
    ]).create_config()
