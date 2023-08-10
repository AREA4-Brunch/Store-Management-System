from abc import abstractmethod, ABC



class Configuration(ABC):
    """ Component in decorator pattern. """

    @abstractmethod
    def __getattr__(self) -> list:
        pass

    @abstractmethod
    def getFlaskAppConfiguration(self):
        pass


class FlaskAppConfigBase(Configuration):
    """ Subject in decorator pattern. """

    def __getattr__(self, attr_name) -> list:
        if not hasattr(self.__class__, attr_name):
            return []
        return [ getattr(self.__class__, attr_name) ]

    def getFlaskAppConfiguration(self):
        return self


class CustomConfigBase(Configuration, ABC):
    """ Decorator in decorator pattern. """

    # private attributes:
    # config: Configuration

    def __init__(self, config: Configuration) -> None:
        self._config = config

    def __getattr__(self, attr_name) -> list:
        attrs = self._config.__getattr__(attr_name)
        if hasattr(self.__class__, attr_name):
            attrs.append(getattr(self.__class__, attr_name))
        return attrs

    def getFlaskAppConfiguration(self):
        return self._config.getFlaskAppConfiguration()
