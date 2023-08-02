from abc import ABC, abstractmethod


class RouteInitializer(ABC):
    """ Interface for callable objects that add routes when
        called to the given app.
    """

    @abstractmethod
    def __call__(self, app) -> None:
        pass
