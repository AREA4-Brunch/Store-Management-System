import importlib

from flask import Flask
from sqlalchemy_utils import database_exists, create_database

from .settings import Settings, FLASK_APP_CONFIGURATION
from . import urls


class App:
    # Private Attributes:
    # app: Flask
    # databases: list
    # route_initializers: list[urls.RouteInitializer]
    # services: dict()

    def __init__(self) -> None:
        """ Creates an app with configuration specified in
            `settings.py`.
        """
        self._config()
        self._init()


    # ====================================================
    # Public Methods:


    def run(self, host='127.0.0.1', port=5000):
        """ [noreturn] Calls run method on created Flask app.
        """
        self._app.run(debug=self._debug, host=host, port=port)

    @property
    def databases(self):
        return self._databases

    @property
    def app(self):
        return self._app

    def __setitem__(self, name, data):
        self._attributes[name] = data

    def __getitem__(self, service_name):
        if service_name == 'app':
            return self._app

        if service_name == 'host':
            return self._app.config['SERVER_NAME'].split(':')[0]

        if service_name == 'port':
            return self._app.config['SERVER_NAME'].split(':')[1]

        return self._attributes[service_name]


    # ====================================================
    # Constructor Helpers:


    def _config(self):
        """ Configures the app based on `settings.py`.
        """
        def config_flask_app():
            self._app = Flask(Settings.APP_NAME or __name__)

            if FLASK_APP_CONFIGURATION:
                self._app.config.from_object(FLASK_APP_CONFIGURATION)

            if Settings.LOGGING_HANDLER is not None:
                for handler in self._app.logger.handlers[:]:
                    self._app.logger.removeHandler(handler)
                self._app.logger.addHandler(Settings.LOGGING_HANDLER)
                self._app.logger.setLevel(FLASK_APP_CONFIGURATION.LOGGING_LEVEL)

        config_flask_app()
        self._debug = Settings.DEBUG
        self._databases = Settings.DATABASES
        self._route_initializers = urls.ROUTE_INITIALIZERS
        self._on_init_configs = Settings.ON_INIT
        self._attributes = dict()

    def _init(self):
        self._init_databases()
        self._on_init()
        self._init_endpoints()

    def _init_databases(self):
        for db_config in self._databases.values():
            db_config["database"].init_app(self._app)
            # db["migrate"].init_app(self._app)

            with self._app.app_context():
                # init the database if the function was provided:
                if "init" in db_config:
                    (module_name, func_name) = db_config["init"]
                    module = importlib.import_module(module_name)
                    func = getattr(module, func_name)
                    func(self, db_config)
                else:  # create fresh new db
                    if not database_exists(db_config['uri']):
                        create_database(db_config['uri'])
                    db_config["database"].create_all()

    def _init_endpoints(self):
        for route_init in self._route_initializers:
            route_init(self)

    def _on_init(self):
        for on_init_config in self._on_init_configs:
            (module_name, func_name) = on_init_config['init']
            module = importlib.import_module(module_name)
            func = getattr(module, func_name)
            func(self, on_init_config)


class UserManagementSystem(App):
    pass
