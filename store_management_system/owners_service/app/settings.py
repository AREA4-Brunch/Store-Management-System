import logging
from libs.flask_app_extended.config import FlaskAppConfigBase


class FlaskAppConfig(FlaskAppConfigBase):
    DEBUG = True

    LOGGING_LEVEL = logging.DEBUG

    # SQLALCHEMY_DATABASE_URI = Settings.DATABASES["users"]["uri"]
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = "JWT_SECRET_DEV_KEY"
    # JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)
    # JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
