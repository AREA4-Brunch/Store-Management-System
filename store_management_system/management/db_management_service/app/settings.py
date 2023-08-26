import logging
from flask_app_extended.config import (
    CustomConfigBase,
    CustomConfigDecoratorBase,
    DefaultConfigFactory,
)
from .commands import store_management_db
from .__secrets import STORE_MANAGEMENT_DB  # in production to replace with env variables



# ========================================================
# Core Configurations Helpers:



class FlaskAppConfig(CustomConfigBase):
    DEBUG = False

    LOGGING_LEVEL = logging.DEBUG

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:{STORE_MANAGEMENT_DB['pwd']}@localhost/store_management"
    SQLALCHEMY_TRACK_MODIFICATIONS = False



class CommandsConfiguration(CustomConfigDecoratorBase):
    _COMMANDS_TO_BIND_PATH = (
        store_management_db.init,
        store_management_db.upgrade_and_populate,
        store_management_db.drop_db,
        store_management_db.drop_upgrade_populate
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
