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


def roles_present(*args_role_req, **kwargs_role_req):
    """ Does not check if the user is logged in, to add that
        to this check use `roles_required_login` instead.
    """
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            failure_response = AuthenticationService \
                .roles_required(*args_role_req,
                                **kwargs_role_req)

            return failure_response \
                or function(*args, **kwargs)

        return wrapper
    return decorator
