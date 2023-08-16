from flask import Flask
from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide
from libs.flask_app_extended.app import DefaultAppFactory
from libs.flask_app_extended.config_utils import (
    DefaultLoggerConfig,
    DefaultBlueprintsConfig
)
from .settings import FlaskAppConfig



def create_app() -> Flask:
    app = DefaultAppFactory(
        FlaskAppConfig,
        [  # config decorators:
            DefaultLoggerConfig,
            DefaultBlueprintsConfig,
        ]
    ).create_app()
    return app


class IoCAppContainer(containers.DeclarativeContainer):
    def __init__(self) -> None:
        super().__init__()
        # config = IoCAppContainer.config()

    # config = providers.Configuration()
    app = providers.Singleton(create_app)


@inject
def get_app(app: Flask=Provide[IoCAppContainer.app]):
    return app
