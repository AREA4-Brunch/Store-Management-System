from libs.flask_app_extended.app import DefaultAppFactory
from .settings import FlaskAppConfig


APP = DefaultAppFactory(FlaskAppConfig).create_app()
