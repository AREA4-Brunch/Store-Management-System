import importlib

from flask import Flask
from flask_jwt_extended import JWTManager

from . import settings
from . import urls


class UserManagementSystem:
    # Private Attributes:
    # app: Flask
    # databases: list
    # route_initializers: list[urls.RouteInitializer]
    # jwt: JWTManager

    def __init__(self) -> None:
        """ Creates an app with configuration specified in
            `settings.py`.
        """
        self._config()
        self._init()


    # ====================================================
    # Public Methods:


    def run(self):
        """ [noreturn] Calls run method on created Flask app.
        """
        self._app.run(debug=self._debug)

    @property
    def databases(self):
        return self._databases

    @property
    def app(self):
        return self._app


    # ====================================================
    # Constructor Helpers:


    def _config(self):
        """ Configures the app based on `settings.py`.
        """
        def config_flask_app():
            self._app = Flask(settings.APP_NAME or __name__)
            if settings.FLASK_APP_CONFIGURATION:
                self._app.config.from_object(settings.FLASK_APP_CONFIGURATION)

            if settings.LOGGING_HANDLER:
                for handler in self._app.logger.handlers[:]:
                    self._app.logger.removeHandler(handler)
                self._app.logger.addHandler(settings.LOGGING_HANDLER)

        config_flask_app()
        self._debug = settings.DEBUG
        self._databases = settings.DATABASES
        self._route_initializers = urls.ROUTE_INITIALIZERS

    def _init(self):
        self._init_databases()
        self._init_endpoints()
        self._init_jwt()

    def _init_databases(self):
        for db in self._databases.values():
            db["database"].init_app(self._app)
            db["migrate"].init_app(self._app)

            with self._app.app_context():
                db["database"].create_all()

                # populate the database if the function was provided:
                if "populate" in db:
                    (module_name, func_name) = db["populate"]
                    module = importlib.import_module(module_name)
                    func = getattr(module, func_name)
                    func(self._app, db["database"])


    def _init_endpoints(self):
        for route_init in self._route_initializers:
            route_init(self)

    def _init_jwt(self):
        self._jwt = JWTManager(self._app)
