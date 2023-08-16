import logging
import redis
from flask import Flask
from libs.flask_app_extended.config import (
    FlaskAppConfigBase,
    CustomConfigBase,
    Configuration
)


class FlaskAppConfig(FlaskAppConfigBase):
    DEBUG = True

    LOGGING_LEVEL = logging.DEBUG

    # SQLALCHEMY_DATABASE_URI = Settings.DATABASES["users"]["uri"]
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = "JWT_SECRET_DEV_KEY"
    # JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)
    # JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)


# class RedisConfig(CustomConfigBase):
#     def __init__(self, config: Configuration) -> None:
#         super().__init__(config)

#     @classmethod
#     def get_on_init(cls, this: CustomConfigBase):
#         def on_init(app: Flask):
#             redis_client = redis.StrictRedis(
#                 host=this.HOST,
#                 port=this.PORT,
#                 db=this.DB,
#                 decode_responses=this.DECODE_RESPONSES
#             )
#         return on_init

#     HOST = '127.0.0.1'
#     PORT = 6379
#     DB = 0
#     DECODE_RESPONSES = True
