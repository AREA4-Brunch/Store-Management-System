from abc import abstractmethod, ABC
from flask import Flask
from .config import Configuration



class AppFactoryBase(ABC):
    @abstractmethod
    def create_app(self) -> Flask:
        pass


class DefaultAppFactory(AppFactoryBase):
    def __init__(self, config: Configuration) -> None:
        super().__init__()
        self._config = config

    def create_app(self) -> Flask:
        app = Flask(__name__)
        app.config.from_object(self._config)
        return app
