from abc import abstractmethod, ABC
from typing import Type
from flask import Flask
from dependency_injector import containers
from flask_app_extended.app import AppFactoryBase
from flask_app_extended.utils.app_utils import DefaultFlaskAppInitializer
from flask_app_extended.config import Configuration



class CommonAppFactoryBase(AppFactoryBase, ABC):
    def __init__(
        self,
        container_type: Type[containers.DeclarativeContainer],
    ) -> None:
        super().__init__()
        self._container_type = container_type

    def create_app(self, modules) -> Flask:
        """ Relies on knowing the structure of given container.
        """
        container, variables = self._init_container(modules)

        # bind routes, commands, call custom initializers
        app = self._initialize_app(
            container,
            variables['core.app'],
            variables['core.flask_app_extended_config']
        )

        return app

    def _init_container(self, modules):
        container = self._container_type()
        container.init_resources()
        container.wire(modules=modules)

        # construct the objects/initialize them through
        # their constructors
        variables = self.construct_container_variables(container)
        return container, variables

    def _initialize_app(
        self,
        container: containers.DeclarativeContainer,
        app: Flask,
        config: Configuration
    ) -> Flask:
        """ Sets app.container = container; and then initializes the app
            using flask_app_extended.DefaultFlaskAppInitializer with
            provided configuration.
            Returns initialized flask.Flask app object.
        """
        app.container = container

        # assuming flask_app config has already been
        # setup in provided app
        app = DefaultFlaskAppInitializer(app, config) \
              .bind_blueprints() \
              .bind_commands() \
              .add_initializers() \
              .init()

        return app

    @abstractmethod
    def construct_container_variables(
        self,
        container: containers.DeclarativeContainer
    ) -> dict:
        """ Returns dictionary containing fields:
                core.app: Flask,
                core.flask_app_extended_config: Configuration
            that will be used by:
                flask_app_extended.DefaultFlaskAppInitializer.
            Also constructs all container variables that need to
            be constructed before app starts getting initialized
            since the providers.Singleton lazily initializes.
        """
        pass
