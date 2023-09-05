import redis
import os
from typing import Callable
from web3 import Web3, HTTPProvider
from web3.eth import Contract
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
from db_store_management.models import create_models
from .settings import AppConfiguration



def get_smart_contracts_native_src(native_src_dir_path) -> dict:
    def get_native_src(file_name):
        file_path = os.path.join(native_src_dir_path, file_name)
        with open(file_path, 'r') as in_file:
            return in_file.read()

    return {
        'OrderPayment': {
            'abi': get_native_src('OrderPayment-0.4.0.abi'),
            'bin': get_native_src('OrderPayment-0.4.0.bin'),
        }
    }


class Core(containers.DeclarativeContainer):
    config = providers.Dependency(instance_of=Configuration)

    app = providers.Singleton(
        lambda config: DefaultAppFactory(config).create_app(),
        config.provided.flask_app
    )

    smart_contracts_native_src_register: dict = providers.Singleton(
        get_smart_contracts_native_src,
        config.provided.smart_contracts.NATIVE_SRC_DIR_PATH
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

    w3: Web3 = providers.Singleton(
        lambda host_uri: Web3(HTTPProvider(host_uri)),
        config.provided.w3.SIMULATOR_URI
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

    db_store_management_models = providers.Singleton(
        create_models,
        db_store_management
    )

    auth = providers.Singleton(
        AuthenticationService,
        app=core.app,
        redis_client=gateways.redis_client_auth
    )

    smart_contracts_factory: Callable = providers.Singleton(
        lambda w3, native_src: (
            lambda contract, address=None: w3.eth.contract(
                address=address,
                abi=native_src[contract]['abi'],
                bytecode=native_src[contract]['bin'],
            )
        ),
        gateways.w3,
        core.smart_contracts_native_src_register
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

            'services.db_store_management':
                container.services.db_store_management(),

            'services.migrate_db_store_management':
                container.services.migrate_db_store_management(),

            'services.db_store_management_models':
                container.services.db_store_management_models(),

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
