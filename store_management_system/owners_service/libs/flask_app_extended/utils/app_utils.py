from typing import Union
from collections.abc import Iterable, Callable
from flask import Flask, Blueprint
from ..config import Configuration
from .utils import load_attr_from_file


class DefaultAppBuilder:
    """ Just a useful utility used by DefaultAppFactory.
        Binds configuration properties to Flask app.
    """

    # private attributes:
    # app: Flask
    # config: Configuration class - selected config src
    # inits: list of callable objects, called on build()

    def __init__(self, active_config_src_class: Configuration=None) -> None:
        self._app = Flask(__name__)
        self._config = active_config_src_class
        self._inits = []

    def build(self) -> Flask:
        for init in self._inits:
            init(self._app)

        return self._app

    @property
    def config_class(self) -> Configuration:
        return self._config

    def setActiveConfigClass(self, config_class: Configuration):
        """ Sets default/failback class used for omitted args in setters. """
        self._config = config_class
        return self

    def setFlaskAppConfig(self, flask_config_class=None):
        config = flask_config_class \
               or self._config.getDecoratedSubject()
        self._app.config.from_object(config)
        return self

    def bindBlueprints(self, url_blueprints: Iterable=None):
        """ url_blueprints can be an iterable containing
            pairs (url_prefix, flask.Blueprint) or iterables
            containing them, or both.
        """
        # if blueprints is not provided load in from
        # files specified in selected configuration class
        if url_blueprints is None:
            blueprints_var_paths: Iterable[str] \
                = self._config.get_all('_BLUEPRINTS_TO_BIND_PATH')

            for blueprints_var_path in blueprints_var_paths:
                url_blueprints = load_attr_from_file(blueprints_var_path)
                if url_blueprints is not None:
                    return self.bindBlueprints(url_blueprints)

        def process_url_blueprints(
            cur_url_prefix: str,
            blueprint_or_list: Union[Blueprint, Iterable]
        ):
            if isinstance(blueprint_or_list, Blueprint):
                self._app.register_blueprint(blueprint_or_list,
                                             url_prefix=cur_url_prefix)
                return

            # else blueprint_or_list is the collection of same structure
            for url_prefix, blueprint_or_list_ in blueprint_or_list:
                process_url_blueprints(cur_url_prefix + url_prefix,
                                       blueprint_or_list_)

        process_url_blueprints('', url_blueprints)
        return self

    def bindCommands(self, commands: Iterable=None):
        """ commands can be an iterable containing
            command functions or such nested iterables.
        """
        # if commands is not provided load in from
        # selected configuration class
        if commands is None:
            commands = self._config.get_all('_COMMANDS_TO_BIND_PATH')

        def process_commands(
            command_or_list: Union[Callable, Iterable]
        ):
            if isinstance(command_or_list, Callable):
                self._app.cli.add_command(command_or_list)
                return

            # else command_or_list is the collection of same structure
            for command_or_list_ in command_or_list:
                process_commands(command_or_list_)

        process_commands(commands)
        return self

    @property
    def initializers(self):
        """ Returns initializers to be executed in FIFO order on build(). """
        return self._inits

    @initializers.setter
    def initializers(self, initilizer_funcs):
        """ Sets initializers to be executed in FIFO order on build(). """
        self._inits = []
        for init in initilizer_funcs:
            self._addInitializer(init)

    def addInitializers(self, initilizer_funcs=None):
        if initilizer_funcs is not None:
            for init in initilizer_funcs:
                self._addInitializer(init)
            return self

        # else not provided so extract from decorated config
        initilizer_funcs_getters = self._config.get_all('get_on_init')
        for getter in initilizer_funcs_getters:
            self._addInitializer(getter(self._config))

        return self

    def _addInitializer(self, initializer_func):
        """ Adds initializers in given order, FIFO execution order. """
        self._inits.append(initializer_func)

    def _removeInitializer(self, val=None, idx: int=None):
        """ Removes an initializer by val if provided, else by idx. """
        if val is not None:
            self._inits.remove(val)
        else:  # only idx was provided
            self._inits.pop(idx)
