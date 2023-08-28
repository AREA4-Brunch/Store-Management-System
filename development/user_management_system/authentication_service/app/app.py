import redis
# import pymysql  # to init SQLAlchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide
from flask_app_extended.app import DefaultAppFactory
from flask_app_extended.config import Configuration
from std_authentication import AuthenticationService
from project_common.utils.app import CommonAppFactoryBase
from db_user_management.models import create_models
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

    # auth database
    db_user_management = providers.Singleton(SQLAlchemy, core.app)

    migrate_db_user_management = providers.Singleton(
        Migrate,
        core.app,
        db_user_management
    )

    db_user_management_models = providers.Singleton(
        create_models,
        db_user_management
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



class AppFactory(CommonAppFactoryBase):
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

            'services.db_user_management':
                container.services.db_user_management(),

            'services.migrate_db_user_management':
                container.services.migrate_db_user_management(),

            'services.db_user_management_models':
                container.services.db_user_management_models(),

            'services.auth':
                container.services.auth(),
        }

        return variables



def create_app():
    app = AppFactory(ApplicationIoCContainer).create_app([
        'app.app', 'pymysql'
    ])
    return app


@inject
def get_app(app: Flask=Provide[ApplicationIoCContainer.core.app]) -> Flask:
    return app
