from functools import wraps
from flask_jwt_extended import get_jwt, jwt_required, \
                               verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError, RevokedTokenError
from flask import jsonify

from typing import Callable, Any



def login_required(
    response_func: Callable[[Exception], Any]=None,
    err_code: int=None,
    reraise: bool=False
):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            try:
                try:
                    verify_jwt_in_request()

                except Exception as e:
                    # use custom response_func if any
                    if response_func is not None:
                        return response_func(e), err_code or 400
                    # handle errors with default messages
                    raise e

            except RevokedTokenError as e:  # token was blocklisted
                if reraise: raise e;
                return jsonify({
                    'message': 'Unknown user.'
                }), err_code or 400

            except NoAuthorizationError as e:
                if reraise: raise e;
                return jsonify({
                    'msg': 'Missing Authorization Header'
                }), err_code or 401

            except Exception as e:
                if reraise: raise e;
                return jsonify({
                    'message': f'Unexpected login error: {e} + {type(e)} + {e.__class__.__name__}'
                }), err_code or 400

            return function(*args, **kwargs)

        return wrapper
    return decorator


def role_required(role_name):
    def decorator(function):
        @jwt_required()
        @wraps(function)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            if role_name not in claims["roles"]:
                return jsonify({
                    'msg': 'Forbidden'
                }), 403

            return function(*args, **kwargs)
        return wrapper
    return decorator
