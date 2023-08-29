import logging
import os
from flask_app_extended.config import (
    CustomConfigBase,
    CustomConfigDecoratorBase,
    DefaultConfigFactory,
)
from flask_app_extended.utils.config_utils import (
    DefaultFlaskAppLoggerConfig,
)
from .__secrets import USER_MANAGEMENT_DB


DB_USER_MANAGEMENT_URI = os.environ.get(
    'DB_USER_MANAGEMENT_URI',
    f"mysql+pymysql://root:{USER_MANAGEMENT_DB['pwd']}@localhost/authentication"
)
PATH_LOGGING_DIR = os.environ.get('PATH_LOGGING_DIR', './logs/')
LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', 'DEBUG')


# ========================================================
# Core Configurations Helpers:



class FlaskAppConfig(CustomConfigBase):
    LOGGING_LEVEL = getattr(logging, LOGGING_LEVEL)

    SQLALCHEMY_DATABASE_URI = DB_USER_MANAGEMENT_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False



class CommandsConfiguration(CustomConfigDecoratorBase):
    def provide_commands_to_bind():
        from .commands import user_management_db
        commands = (
            user_management_db.init,
            user_management_db.upgrade_and_populate,
            user_management_db.drop_db,
            user_management_db.drop_upgrade_populate
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
