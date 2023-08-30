import os
import logging
from flask_app_extended.config import (
    CustomConfigBase,
    CustomConfigDecoratorBase,
    DefaultConfigFactory,
)
from flask_app_extended.utils.config_utils import (
    DefaultFlaskAppLoggerConfig,
)
from .__secrets import STORE_MANAGEMENT_DB  # in production to replace with env variables


DB_STORE_MANAGEMENT_URI = os.environ.get(
    'DB_STORE_MANAGEMENT_URI',
    f"mysql+pymysql://root:{STORE_MANAGEMENT_DB['pwd']}@localhost/store_management"
)
PATH_LOGGING_DIR = os.environ.get('PATH_LOGGING_DIR', './logs/')
LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', 'DEBUG')




# ========================================================
# Core Configurations Helpers:



class FlaskAppConfig(CustomConfigBase):
    LOGGING_LEVEL = getattr(logging, LOGGING_LEVEL)

    SQLALCHEMY_DATABASE_URI = DB_STORE_MANAGEMENT_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class CommandsConfiguration(CustomConfigDecoratorBase):
    def provide_commands_to_bind():
        from .commands import store_management_db
        commands = (
            store_management_db.init,
            store_management_db.upgrade_and_populate,
            store_management_db.drop_db,
            store_management_db.drop_upgrade_populate
        )
        return commands

    _COMMANDS_TO_BIND_PROVIDER = provide_commands_to_bind


class FileLoggerConfig(DefaultFlaskAppLoggerConfig):
    LOG_FILE_PATH = os.path.join(PATH_LOGGING_DIR, 'log1.log')



# ========================================================
# App Configuration:



class CoreConfiguration(CustomConfigDecoratorBase):
    flask_app = FlaskAppConfig()

    # flask_app_extended lib's settings assume in
    # app_utils.DefaultAppInitializer
    flask_app_extended = DefaultConfigFactory(flask_app, [
        FileLoggerConfig,
        CommandsConfiguration
    ]).create_config()


class AppConfiguration(CustomConfigBase):
    core = DefaultConfigFactory(CustomConfigBase(), [
        CoreConfiguration,
    ]).create_config()
