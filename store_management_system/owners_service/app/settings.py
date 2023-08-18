import logging
from libs.flask_app_extended.config import (
    CustomConfigBase,
    CustomConfigDecoratorBase,
    DefaultConfigFactory,
)
from .management.commands import store_management_db
from .__secrets import STORE_MANAGEMENT_DB  # in production to replace with env variables


# ========================================================
# Core Configurations Helpers:



from libs.flask_app_extended.utils.config_utils import (
    DefaultFlaskAppLoggerConfig,
    DefaultURLBlueprintsConfig,
)



class FlaskAppConfig(CustomConfigBase):
    DEBUG = True

    LOGGING_LEVEL = logging.DEBUG

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:{STORE_MANAGEMENT_DB['pwd']}@localhost/store_management"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = "JWT_SECRET_DEV_KEY"
    # JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)
    # JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)



class CommandsConfiguration(CustomConfigDecoratorBase):
    _COMMANDS_TO_BIND_PATH = (
        store_management_db.upgrade_and_populate,
    )



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
        DefaultURLBlueprintsConfig,
        CommandsConfiguration
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
