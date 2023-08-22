from functools import wraps
from .services import AuthenticationService


def login_required(*args_login, **kwargs_login):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            failure_response = AuthenticationService \
                .login_required(*args_login, **kwargs_login)

            return failure_response \
                or function(*args, **kwargs)

        return wrapper
    return decorator


def roles_required_login(*args_login, **kwargs_login):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            failure_response = AuthenticationService \
                .roles_required_login(*args_login, **kwargs_login)

            return failure_response \
                or function(*args, **kwargs)

        return wrapper
    return decorator
