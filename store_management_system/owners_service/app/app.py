import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide
from libs.flask_app_extended.app import DefaultAppFactory, AppFactoryBase
from libs.flask_app_extended.utils.app_utils import DefaultFlaskAppInitializer
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
    db_store_management = providers.Singleton(SQLAlchemy, core.app)

    migrate_db_store_management = providers.Singleton(
        Migrate,
        core.app,
        db_store_management
    )

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


class AppFactory(AppFactoryBase):
    def __init__(self) -> None:
        super().__init__()

    def create_app(
        self,
        container: containers.DeclarativeContainer
    ) -> Flask:
        """ Relies on knowing the structure of given container.
        """
        self._init_container(container)

        # bind routes, commands, call custom initializers
        app = self._initialize_app(
            container,
            container.core.config().flask_app_extended
        )

        return app

    def _init_container(self, container):
        container.init_resources()
        container.wire(modules=[ 'app.app' ])

        # construct the objects/initialize them through
        # their constructors
        variables = self._construct_container_variables(container)

    def _construct_container_variables(self, container) -> dict:
        # singleton is lazily initialized so request it now
        # so everything gets created/initilized with their
        # constructors
        variables = {
            'core.flask_app_extended_config':
                container.core.config().flask_app_extended,

            'core.app':
                container.core.app(),

            'gateways.redis_client_auth':
                container.gateways.redis_client_auth(),

            'services.db_store_management':
                container.services.db_store_management(),

            'services.migrate_db_store_management':
                container.services.migrate_db_store_management(),

            'services.auth':
                container.services.auth(),
        }

        return variables

    def _initialize_app(
        self,
        container: containers.DeclarativeContainer,
        config: Configuration
    ) -> Flask:
        app = container.core.app()
        app.container = container

        # assuming flask_app config has already been
        # setup in provided app
        app = DefaultFlaskAppInitializer(app, config) \
              .bind_blueprints() \
              .bind_commands() \
              .add_initializers() \
              .init()

        return app

def create_app():
    app  = AppFactory().create_app(ApplicationIoCContainer())
    return app


@inject
def get_app(app: Flask=Provide[ApplicationIoCContainer.core.app]) -> Flask:
    return app
