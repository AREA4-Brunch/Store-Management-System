from typing import Callable, Any, Iterable
from redis import Redis
from flask import Flask, jsonify
from flask_jwt_extended import (
    JWTManager,
    get_jwt,
    jwt_required,
    verify_jwt_in_request,
    get_jwt_identity
)
from flask_jwt_extended.exceptions import NoAuthorizationError, \
                                          RevokedTokenError
from .utils import get_expiry_hour



class AuthenticationService:
    def __init__(self, app: Flask, redis_client: Redis) -> None:
        self._app = app
        self._redis_client = redis_client
        self._init_jwt()

    def _init_jwt(self):
        self._jwt = JWTManager(self._app)

        # add redis blocklist checker to jwt_required feature
        @self._jwt.token_in_blocklist_loader
        def is_jwt_in_blocklist(jwt_header: dict, jwt_payload: dict) -> bool:
            jti = jwt_payload['jti']
            expiry_hour, time_format = get_expiry_hour(jwt_payload)
            blocklist_group = f'jwt_blk:exp={expiry_hour}'
            return self._redis_client.sismember(blocklist_group, jti)

    @staticmethod
    def login_required(
        response_func: Callable[[Exception], Any]=None,
        err_code: int=None,
        reraise: bool=False,
        **kwargs
    ):
        """ Returns None in case the user is logged in properly,
            else returns appropriate, jsonified response.
        """
        try:
            try:
                verify_jwt_in_request()

            except Exception as e:
                # use custom response_func if any
                if response_func is not None:
                    return response_func(e)
                # else handle errors with default messages or reraise
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
                'message':
                    f'Unexpected login error: {e} + {type(e)} + {e.__class__.__name__}'
            }), err_code or 400

        return None

    @staticmethod
    def roles_required(
        roles_names: Iterable[str],
        roles_response_func: Callable[[dict], Any] \
            =lambda _: (jsonify({'msg': 'Forbidden'}), 403),
        roles_required_cnt=1,
        **kwargs
    ):
        """ Returns None in case default or given number of given
            roles is satisfied, else returns default or given
            response to which it passes as arg the dict of the
            roles present in the request's jwt.
        """
        claims = get_jwt()
        for role_name in roles_names:
            if role_name in claims["roles"]:
                roles_required_cnt -= 1
                if roles_required_cnt <= 0:
                    return None  # allowed, has the role_name

        return roles_response_func(claims['roles'])

    @staticmethod
    def roles_required_login(*args, **kwargs):
        """ Returns None in case one of the given roles is satisfied
            and the user is logged in,
            else returns appropriate, jsonified response.
        """
        return AuthenticationService.login_required(**kwargs) \
            or AuthenticationService.roles_required(*args[ : 1], **kwargs)

    @staticmethod
    def get_user_identifier_from_jwt_header():
        email = get_jwt_identity()
        return email
