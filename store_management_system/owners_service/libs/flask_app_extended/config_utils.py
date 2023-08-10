import logging
from typing import Type
from flask import Flask
from .config import Configuration, CustomConfigBase


class DefaultLoggerConfig(CustomConfigBase):
    """ Concrete Decorator in decorator pattern. """

    def __init__(self, config: Configuration) -> None:
        super().__init__(config)

    @classmethod
    def get_on_init(cls):
        def on_init(app: Flask):
            logging.basicConfig(
                filename=cls.LOG_FILE_PATH,
                level=logging.INFO,
                format='%(asctime)s [%(levelname)s] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        return on_init

    LOG_FILE_PATH = f'./logs/log1.log'


class DefaultBlueprintsConfig(CustomConfigBase):
    def __init__(self, config: Configuration) -> None:
        super().__init__(config)

    # path to pbject that can be an iterable containing pairs
    # (url_prefix, flask.Blueprint) or iterables containing
    # them, or both.
    URL_BLUEPRINTS_PATH = 'app.urls.url_blueprints'


class DefaultConfigurationBuilder:
    def __init__(self, flask_app_config: Configuration) -> None:
        self._config = flask_app_config

    def build(self) -> Configuration:
        return self._config

    def addLoggingConfig(
        self,
        logger_cls: Type[CustomConfigBase]=DefaultLoggerConfig
    ):
        self._config = logger_cls(self._config)
        return self

    def addBlueprintsConfig(
        self,
        logger_cls: Type[CustomConfigBase]=DefaultBlueprintsConfig
    ):
        self._config = logger_cls(self._config)
        return self
