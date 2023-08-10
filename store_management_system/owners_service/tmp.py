from abc import abstractmethod, ABC


class Configuration(ABC):
    """ Component in decorator pattern. """

    @abstractmethod
    def __getattr__(self) -> list:
        pass


class DefaultFlaskAppConfig(Configuration):
    """ Subject in decorator pattern. """

    def __getattr__(self, attr_name) -> list:
        if not hasattr(self.__class__, attr_name):
            return []
        return [ getattr(self.__class__, attr_name) ]


class CustomConfig(Configuration, ABC):
    """ Decorator in decorator pattern. """

    # private attributes
    # config

    def __init__(self, config: Configuration) -> None:
        self._config = config

    def __getattr__(self, attr_name) -> list:
        attrs = self._config.__getattr__(attr_name)
        if hasattr(self.__class__, attr_name):
            attrs.append(getattr(self.__class__, attr_name))
        return attrs


class LoggerConfiguration(CustomConfig):
    """ Concrete Decorator in decorator pattern. """

    def __init__(self, config: Configuration) -> None:
        super().__init__(config)


    URL_BLUEPRINTS_PATH = 'urls.url_blueprints'



def main():
    config = LoggerConfiguration(DefaultFlaskAppConfig())
    print(f'Hi: {getattr(config, "URL_BLUEPRINTS_PATH")}')
    return


if __name__ == '__main__':
    main()

