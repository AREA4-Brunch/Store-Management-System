from abc import abstractmethod, ABC
from flask import Flask
from libs.flask_app_extended.config import Configuration
from .config import Configuration
from .utils.app_utils import DefaultAppBuilder



class AppFactoryBase(ABC):
    @abstractmethod
    def create_app(self) -> Flask:
        pass


class DefaultAppFactory(AppFactoryBase):
    def __init__(self, config: Configuration) -> None:
        super().__init__()
        self._config = config

    def create_app(self) -> Flask:
        app = DefaultAppBuilder(self._config) \
              .setFlaskAppConfig() \
              .bindBlueprints() \
              .bindCommands() \
              .addInitializers() \
              .build()

        return app
