from .endpoints.RegistrationRouteInitializer import RegistrationRouteInitializer
from .endpoints.LoginRouteInitializer import LoginRouteInitializer


ROUTE_INITIALIZERS = [
    RegistrationRouteInitializer(),
    LoginRouteInitializer()
]
