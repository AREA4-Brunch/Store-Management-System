import logging
from flask import Flask
from ..config import CustomConfigDecoratorBase



class DefaultFlaskAppLoggerConfig(CustomConfigDecoratorBase):
    """ Concrete Decorator in decorator pattern.
        Decorates config, adds new logger handler to
        flask.Flask app when on_init is called.
    """

    @classmethod
    def get_on_init(cls, this: CustomConfigDecoratorBase):
        def on_init(app: Flask):
            log_level = app.config['LOGGING_LEVEL']
            file_path = this.LOG_FILE_PATH  # <=> cls.LOG_FILE_PATH[0],
            format = this.FORMAT
            datefmt = this.DATEFMT

            file_handler = logging.FileHandler(file_path)
            file_handler.setLevel(log_level)
            formatter = logging.Formatter(format, datefmt=datefmt)
            file_handler.setFormatter(formatter)
            app.logger.addHandler(file_handler)

            print(f'Configured app logging, linked to file:\n{file_path}\n')
            app.logger.info(
                f'Configured app logging, linked to file:\n{file_path}\n'
            )

        return on_init

    # Attributes:

    LOG_FILE_PATH = f'./logs/log1.log'
    FORMAT = r'%(asctime)s [%(levelname)s] %(message)s'
    DATEFMT = '%Y-%m-%d %H:%M:%S'



class DefaultGlobalLoggerConfig(CustomConfigDecoratorBase):
    """ Concrete Decorator in decorator pattern.
        Decorates config, configures global logging module
        when on_init is called.
    """

    @classmethod
    def get_on_init(cls, this: CustomConfigDecoratorBase):
        def on_init(app: Flask):
            file_path = this.LOG_FILE_PATH  # <=> cls.LOG_FILE_PATH[0],
            format = this.FORMAT
            log_level = this.LOGGER_LEVEL
            datefmt = this.DATEFMT

            logging.basicConfig(
                filename=file_path,
                level=log_level,
                format=format,
                datefmt=datefmt
            )

            print(f'Configured global logging, linked to file:\n{file_path}\n')
            logging.info(
                f'Configured global logging, linked to file:\n{file_path}\n'
            )

        return on_init

    # Attributes:

    LOG_FILE_PATH = f'./logs/log1.log'
    LOGGER_LEVEL = logging.DEBUG
    FORMAT = r'%(asctime)s [%(levelname)s] %(message)s'
    DATEFMT = '%Y-%m-%d %H:%M:%S'



class DefaultURLBlueprintsConfig(CustomConfigDecoratorBase):
    # path to pbject that can be an iterable containing pairs
    # (url_prefix, flask.Blueprint) or iterables containing
    # them, or both.
    _BLUEPRINTS_TO_BIND_PATH = 'app.urls.url_blueprints'
