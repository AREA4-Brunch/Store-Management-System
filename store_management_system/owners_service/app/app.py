from libs.flask_app_extended.app import DefaultAppFactory
from libs.flask_app_extended.config_utils import (
    DefaultLoggerConfig,
    DefaultBlueprintsConfig
)
from .settings import FlaskAppConfig



APP = DefaultAppFactory(
    FlaskAppConfig,
    [  # config decorators:
        DefaultLoggerConfig,
        DefaultBlueprintsConfig,
    ]
).create_app()
