import logging
from flask import Flask
from dependency_injector import providers, containers
from dependency_injector.wiring import inject, Provide
from . import config
from .settings import init_logger
from .spark_apps.product_statistics.app import ProductStatisticsApp
from .spark_apps.category_statistics.app import CategoryStatisticsApp



class AppContainer(containers.DeclarativeContainer):
    config = providers.Dependency(dict)

    app = providers.Singleton(Flask, __name__)
    logger = providers.Singleton(init_logger, app)

    cur_config = config.provided['product_statistics']
    product_statistics = providers.Singleton(
        ProductStatisticsApp,
        cur_config.PATH_MYSQL_CONNECTOR_JAR,
        cur_config.SPARK_MASTER_URL,
        cur_config.DB_STORE_MANAGEMENT_URI,
        path_spark_app_file=cur_config.PATH_SPARK_APP_PY
    )

    cur_config = config.provided['category_statistics']
    category_statistics = providers.Singleton(
        CategoryStatisticsApp,
        cur_config.PATH_MYSQL_CONNECTOR_JAR,
        cur_config.SPARK_MASTER_URL,
        cur_config.DB_STORE_MANAGEMENT_URI,
        path_spark_app_file=cur_config.PATH_SPARK_APP_PY
    )


def create_app() -> Flask:
    config_ = {
        'product_statistics': config.product_statistics,
        'category_statistics': config.category_statistics,
    }

    container = AppContainer(config=config_)
    container.init_resources()
    container.wire(modules=[ __name__ ])
    app = container.app()
    # create instances of dependant classes whose static methods
    # depends on initialization/injection: HERE
    app.container = container
    register_endpoints(app)

    return app


def register_endpoints(app: Flask):
    """ Dynamic import to avoid cyclical import as endpoints may
        depend on AppContainer class.
    """
    from .api import register_endpoints as register_endpoints_
    register_endpoints_(app)


@inject
def get_app(app: Flask=Provide[AppContainer.app]) -> Flask:
    return app
