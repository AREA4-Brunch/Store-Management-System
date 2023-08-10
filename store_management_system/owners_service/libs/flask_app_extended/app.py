from abc import abstractmethod, ABC
from typing import Type
from flask import Flask
from .config import Configuration, CustomConfigBase
from .app_utils import DefaultAppBuilder
from .config_utils import (
    DefaultConfigurationBuilder,
    DefaultLoggerConfig,
    DefaultBlueprintsConfig,
)



class AppFactoryBase(ABC):
    @abstractmethod
    def create_app(self) -> Flask:
        pass


class ConfigFactoryBase(ABC):
    @abstractmethod
    def create_config(self) -> Configuration:
        pass


class DefaultAppFactory(AppFactoryBase):
    def __init__(
        self,
        flask_app_config_cls: Type[Configuration],
        logging_config_cls: Type[CustomConfigBase]=DefaultLoggerConfig,
        blueprints_config_cls: Type[CustomConfigBase]=DefaultBlueprintsConfig
    ) -> None:
        super().__init__()
        self._flask_app_config_cls = flask_app_config_cls
        self._logging_config_cls = logging_config_cls
        self._blueprints_config_cls = blueprints_config_cls

    def create_app(self) -> Flask:
        config = DefaultConfigurationBuilder(self._flask_app_config_cls) \
                .addLoggingConfig(self._logging_config_cls) \
                .addBlueprintsConfig(self._blueprints_config_cls) \
                .build()

        app = DefaultAppBuilder(config) \
              .setFlaskAppConfig() \
              .bindBlueprints() \
              .build()

        return app
