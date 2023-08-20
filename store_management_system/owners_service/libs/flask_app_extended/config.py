from abc import abstractmethod, ABC
from typing import Type



class Configuration(ABC):
    """ Component in decorator pattern. """

    @abstractmethod
    def __getattr__(self, attr_name: str):
        """ Invoked only if attr_name was not found in this object. """
        pass

    @abstractmethod
    def get_all(self, attr_name) -> list:
        pass

    @abstractmethod
    def get_decorated_subject(self):
        pass


class CustomConfigBase(Configuration):
    """ Subject in decorator pattern. """

    def __getattr__(self, attr_name: str):
        """ Invoked only if attr_name was not found in this object. """
        # raise KeyError(f'{self.__class__.__name__} has no attribute called: {attr_name}')
        if hasattr(self.__class__, attr_name):  # check class
            return getattr(self.__class__, attr_name)

        return super().__getattr__(attr_name)

    def get_all(self, attr_name) -> list:
        if not hasattr(self.__class__, attr_name):
            return []
        return [ getattr(self.__class__, attr_name) ]

    def get_decorated_subject(self):
        return self


class CustomConfigDecoratorBase(Configuration):
    """ Decorator in decorator pattern. """

    # private attributes:
    # config: Configuration

    def __init__(self, config: Configuration) -> None:
        self._config = config

    def __getattr__(self, attr_name: str):
        """ Invoked only if attr_name was not found in this object.
            Returns the result of the search in decorated config.
        """
        if hasattr(self.__class__, attr_name):  # check class
            return getattr(self.__class__, attr_name)

        return self._config.__getattr__(attr_name)

    def get_all(self, attr_name) -> list:
        attrs = self._config.get_all(attr_name)
        if hasattr(self.__class__, attr_name):
            attrs.append(getattr(self.__class__, attr_name))
        return attrs

    def get_decorated_subject(self):
        return self._config.get_decorated_subject()


class ConfigFactoryBase(ABC):
    @abstractmethod
    def create_config(self) -> Configuration:
        pass


class DefaultConfigFactory(ConfigFactoryBase):
    def __init__(
        self,
        config_base_obj: Configuration,
        additional_config_classes: list[Type[Configuration]]=[]
            # = [DefaultLoggerConfig, DefaultBlueprintsConfig],
    ) -> None:
        super().__init__()
        self._config_base_obj = config_base_obj
        self._additional_config_classes = additional_config_classes

    def create_config(self) -> Configuration:
        config = DefaultConfigurationBuilder(self._config_base_obj)

        for config_cls in self._additional_config_classes:
            config.add(config_cls)

        config = config.build()
        return config


class ConfigurationBuilderBase(ABC):
    @abstractmethod
    def build(self) -> Configuration:
        pass


class DefaultConfigurationBuilder(ConfigurationBuilderBase):
    def __init__(self, flask_app_config_obj: Configuration) -> None:
        super().__init__()
        self._config = flask_app_config_obj

    def build(self) -> Configuration:
        return self._config

    def add(self, config_cls: Type[Configuration]):
        self._config = config_cls(self._config)
