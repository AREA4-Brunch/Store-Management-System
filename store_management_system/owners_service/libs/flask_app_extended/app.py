from abc import abstractmethod, ABC
from flask import Flask
from .config import Configuration


class AppFactoryBase(ABC):
    @abstractmethod
    def create_app(self, config: Configuration) -> Flask:
        pass


class ConfigFactoryBase(ABC):
    @abstractmethod
    def create_config(self, flask_app_config: Configuration) -> Configuration:
        pass
