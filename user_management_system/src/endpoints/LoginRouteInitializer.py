from flask import request as flask_request
from flask import jsonify
from flask_jwt_extended import get_jwt_header

from ..models import User
from .RouteInitializer import RouteInitializer
from .utils import is_valid_email_format, generate_jwts, is_logged_in


class LoginRouteInitializer(RouteInitializer):
    def __call__(self, app) -> None:
        """ Init all the user management system endpoints for given app.
        """
        logger = app.app.logger
        # db = app.databases["users"]["database"]

        # ==================================================
        # Endpoints:

        @app.app.route('/login', methods=["POST"])
        def login():
            return login_user_view()

        # ==================================================
        # Helpers:

        def login_user_view():
            class UserDoesNotExist(Exception):
                pass

            class ParsingError(Exception):
                pass

            class ValidationError(Exception):
                pass

            def parse_login_form():
                data = dict({
                    "email": flask_request.json.get("email", ''),
                    "password": flask_request.json.get("password", ''),
                })

                # check if all required fields have been filled out
                def check_missing_fields():
                    for field_name, field_val in data.items():
                        if field_val is None or len(field_val) == 0:
                            raise ParsingError(f'Field {field_name} is missing.')

                check_missing_fields()
                # TODO: check for too long fields, > 256 chars
                return data

            def validate_login_form(data):
                def validate_email():
                    if len(data["email"]) > 256 \
                    or not is_valid_email_format(data["email"]):
                        raise ValidationError('Invalid email.')

                def validate_password():
                    if not 8 <= len(data["password"]) <= 256:
                        raise ValidationError('Invalid password.')

                validate_email()
                # validate_password()

            try:
                # in case user is already logged in then do not login again
                if is_logged_in()[0]:
                    access_token = flask_request.headers.get('Authorization')\
                                                .replace('Bearer ', '')
                    return jsonify({ "accessToken": access_token }), 200

                data = parse_login_form()
                validate_login_form(data)

                # authenticate the user
                user = User.query.filter_by(
                    email=data["email"],
                    password=data["password"],
                ).first()

                if user is None:
                    raise UserDoesNotExist('Invalid credentials.')

                access_token, refresh_token, claims = generate_jwts(user)

                return jsonify({
                    "accessToken": access_token
                }), 200

            except ParsingError as e:
                return jsonify({
                    "message": f'{e}'
                }), 400

            except ValidationError as e:
                return jsonify({
                    "message": f'{e}'
                }), 400

            except UserDoesNotExist as e:
                return jsonify({
                    "message": f'{e}'
                }), 400

            except Exception as e:  # unexpected error
                logger.exception(f'Failed to login')
                return f'Internal error: {e}', 500
