import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide
from libs.flask_app_extended.app import DefaultAppFactory
from libs.flask_app_extended.config import Configuration
from libs.authentication import AuthenticationService
from .settings import AppConfiguration



class Core(containers.DeclarativeContainer):
    config = providers.Dependency(instance_of=Configuration)

    app = providers.Singleton(
        lambda config: DefaultAppFactory(config).create_app(),
        config.provided.flask_app
    )


class Gateways(containers.DeclarativeContainer):
    config = providers.Dependency(instance_of=Configuration)

    redis_client_auth = providers.Singleton(
        redis.StrictRedis,
        host=config.provided.redis.auth.HOST,
        port=config.provided.redis.auth.PORT,
        db=config.provided.redis.auth.DB,
        decode_responses=config.provided.redis.auth.DECODE_RESPONSES
    )


class Services(containers.DeclarativeContainer):
    config = providers.Dependency(instance_of=Configuration)
    core = providers.DependenciesContainer()
    gateways = providers.DependenciesContainer()

    # store's database
    db_store = providers.Singleton(SQLAlchemy, core.app)

    auth = providers.Singleton(
        AuthenticationService,
        app=core.app,
        redis_client=gateways.redis_client_auth
    )


class ApplicationIoCContainer(containers.DeclarativeContainer):
    config = providers.Singleton(AppConfiguration)

    core = providers.Container(
        Core,
        config=config.provided.core
    )

    gateways = providers.Container(
        Gateways,
        config=config.provided.gateways
    )

    services = providers.Container(
        Services,
        config=config.provided.services,
        core=core,
        gateways=gateways
    )


def create_app() -> Flask:
    container = ApplicationIoCContainer()
    container.init_resources()
    # container.core.init_resources()
    container.wire(modules=[ 'app.app', ])

    return container.core.app()


@inject
def get_app(app: Flask=Provide[ApplicationIoCContainer.core.app]) -> Flask:
    return app
