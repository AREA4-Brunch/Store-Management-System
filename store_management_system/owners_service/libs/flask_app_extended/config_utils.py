import logging
from typing import Type
from flask import Flask
from .config import Configuration, CustomConfigBase


class DefaultLoggerConfig(CustomConfigBase):
    """ Concrete Decorator in decorator pattern. """

    def __init__(self, config: Configuration) -> None:
        super().__init__(config)

    @classmethod
    def get_on_init(cls, this: CustomConfigBase):
        def on_init(app: Flask):
            logging.basicConfig(
                filename=cls.LOG_FILE_PATH,  # <=> this.LOG_FILE_PATH[0],
                level=logging.INFO,
                format='%(asctime)s [%(levelname)s] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            logging.error('Configured')
            print('Configured')
        return on_init

    LOG_FILE_PATH = f'./logs/log1.log'


class DefaultBlueprintsConfig(CustomConfigBase):
    def __init__(self, config: Configuration) -> None:
        super().__init__(config)

    # path to pbject that can be an iterable containing pairs
    # (url_prefix, flask.Blueprint) or iterables containing
    # them, or both.
    URL_BLUEPRINTS_PATH = 'app.urls.url_blueprints'
