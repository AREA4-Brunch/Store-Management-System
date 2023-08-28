from flask import (
    request as flask_request,
    current_app,
    jsonify,
)
from flask_sqlalchemy import SQLAlchemy
from project_common.utils.request import (
    flask_request_get_typechecked as req_get_typechecked
)
from . import USER_ACCOUNT_MANAGEMENT_BP
from ..models import User
from .utils import (
    is_valid_email_format,
    is_logged_in,
    generate_jwts,
)



@USER_ACCOUNT_MANAGEMENT_BP.route('/login', methods=['POST'])
def login_user():
    # db: SQLAlchemy = current_app.container.services.db_user_management()
    logger = current_app.logger

    class UserDoesNotExist(Exception):
        pass

    class ParsingError(Exception):
        pass

    class ValidationError(Exception):
        pass

    def parse_login_form():
        data = dict({
            'email': req_get_typechecked('json', str, 'email', None),
            'password': req_get_typechecked('json', str, 'password', None)
        })

        # check if all required fields have been filled out
        def check_missing_fields():
            for field_name, field_val in data.items():
                if field_val is None or len(field_val) == 0:
                    raise ParsingError(f'Field {field_name} is missing.')

        check_missing_fields()
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
        # TODO: check for too long fields, > 256 chars
        # validate_password()

    try:
        # in case user is already logged in then do not login again
        if is_logged_in()[0]:
            access_token = flask_request.headers \
                            .get('Authorization') \
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
