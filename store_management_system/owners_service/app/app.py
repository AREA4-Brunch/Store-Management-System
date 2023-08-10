from libs.flask_app_extended.app_utils import (
    DefaultAppFactory, DefaultConfigFactory
)
from .settings import FlaskAppConfig



APP = DefaultAppFactory().create_app(
    DefaultConfigFactory().create_config(FlaskAppConfig())
)
