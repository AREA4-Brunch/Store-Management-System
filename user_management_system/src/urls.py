from .endpoints.RegistrationRouteInitializer import RegistrationRouteInitializer
from .endpoints.LoginRouteInitializer import LoginRouteInitializer
from .endpoints.DeleteUserRouteInitializer import DeleteUserRouteInitializer


ROUTE_INITIALIZERS = [
    RegistrationRouteInitializer(),
    LoginRouteInitializer(),
    DeleteUserRouteInitializer()
]
