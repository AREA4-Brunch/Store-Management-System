import logging
import os
from flask_app_extended.config import (
    CustomConfigBase,
    CustomConfigDecoratorBase,
    DefaultConfigFactory,
)
from .commands import user_management_db
from .__secrets import USER_MANAGEMENT_DB


DB_USER_MANAGEMENT_URI = os.environ.get(
    'DB_USER_MANAGEMENT_URI',
    f"mysql+pymysql://root:{USER_MANAGEMENT_DB['pwd']}@localhost/authentication"
)


# ========================================================
# Core Configurations Helpers:



class FlaskAppConfig(CustomConfigBase):
    LOGGING_LEVEL = logging.DEBUG

    SQLALCHEMY_DATABASE_URI = DB_USER_MANAGEMENT_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False



class CommandsConfiguration(CustomConfigDecoratorBase):
    _COMMANDS_TO_BIND_PATH = (
        user_management_db.init,
        user_management_db.upgrade_and_populate,
        user_management_db.drop_db,
        user_management_db.drop_upgrade_populate
    )



# ========================================================
# App Configuration:



class CoreConfiguration(CustomConfigDecoratorBase):
    flask_app = FlaskAppConfig()

    # flask_app_extended lib's settings assume in
    # app_utils.DefaultAppInitializer
    flask_app_extended = DefaultConfigFactory(flask_app, [
        CommandsConfiguration
    ]).create_config()


class AppConfiguration(CustomConfigBase):
    core = DefaultConfigFactory(CustomConfigBase(), [
        CoreConfiguration,
    ]).create_config()
