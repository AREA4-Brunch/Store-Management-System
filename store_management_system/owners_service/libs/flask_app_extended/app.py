from abc import abstractmethod, ABC
from typing import Type
from flask import Flask
from .config import Configuration
from .app_utils import DefaultAppBuilder
from .config import DefaultConfigurationBuilder
from .config_utils import (
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
        additional_config_classes: list[Type[Configuration]] \
            = [DefaultLoggerConfig, DefaultBlueprintsConfig],
    ) -> None:
        super().__init__()
        self._flask_app_config_cls = flask_app_config_cls
        self._additional_config_classes = additional_config_classes

    def create_app(self) -> Flask:
        config = DefaultConfigurationBuilder(self._flask_app_config_cls)

        for config_cls in self._additional_config_classes:
            config.add(config_cls)

        config = config.build()

        app = DefaultAppBuilder(config) \
              .setFlaskAppConfig() \
              .bindBlueprints() \
              .addInitializers() \
              .build()

        return app
