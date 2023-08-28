from flask import (
    # request as flask_request,
    current_app,
    jsonify,
)
from flask_sqlalchemy import SQLAlchemy
from pymysql.err import IntegrityError as pymysql_IntegrityError
from sqlalchemy.exc import IntegrityError as sqlalchemy_IntegrityError
from project_common.utils.request import (
    flask_request_get_typechecked as req_get_typechecked
)
from . import USER_ACCOUNT_MANAGEMENT_BP
from ..models import User, Role, HasRole
from .utils import is_valid_email_format




@USER_ACCOUNT_MANAGEMENT_BP.route('/register_customer', methods=['POST'])
def register_customer():
    return register_user_view(role_name='customer')


@USER_ACCOUNT_MANAGEMENT_BP.route('/register_courier', methods=['POST'])
def register_courier():
    return register_user_view(role_name='courier')


def register_user_view(role_name):
    db: SQLAlchemy = current_app.container.services.db_user_management()
    logger = current_app.logger

    class ParsingError(Exception):
        pass

    class ValidationError(Exception):
        pass

    def parse_registration_form():
        data = dict({
            # 'forename': flask.request.json.get('forename', None)
            'forename': req_get_typechecked('json', str, 'forename', None),
            'surname':  req_get_typechecked('json', str, 'surname', None),
            'email':    req_get_typechecked('json', str, 'email', None),
            'password': req_get_typechecked('json', str, 'password', None),
        })

        # check if all required fields have been filled out
        def check_missing_fields():
            for field_name, field_val in data.items():
                if field_val is None or len(field_val) == 0:
                    raise ParsingError(f'Field {field_name} is missing.')

        check_missing_fields()
        return data

    def validate_registration_form(data):
        def validate_email():
            if not is_valid_email_format(data["email"]) \
            or not (1 <= len(data['email']) <= 256):
                raise ValidationError('Invalid email.')

        def validate_password():
            if not 8 <= len(data["password"]) <= 256:
                raise ValidationError('Invalid password.')

        # TODO: check forename, surname if len > 256 chars
        validate_email()
        validate_password()

    try:
        data = parse_registration_form()
        validate_registration_form(data)

        # add the user to the db along with its role
        user = User(
            forename=data["forename"],
            surname=data["surname"],
            email=data["email"],
            password=data["password"]
        )

        try:
        # with db.session.begin_nested():
            # try to add user (without cost of querying if exists)
            db.session.add(user)
            db.session.flush()

            role = Role.query.filter_by(name=role_name).first()
            # fetch role hence make sure it does not get deleted before commit
            # role = db.session.query(Role).with_for_update() \
            #          .filter_by(name=role_name) \
            #          .one()
            has_role = HasRole(user_id=user.id, role_id=role.id)
            db.session.add(has_role)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            raise e

        # user successfuly created in db
        return '', 200

    except ParsingError as e:
        return jsonify({
            "message": f'{e}'
        }), 400

    except ValidationError as e:
        return jsonify({
            "message": f'{e}'
        }), 400

    # violated UNIQUE db column restriction
    except (
        sqlalchemy_IntegrityError,
        pymysql_IntegrityError
    ) as e:
        err_msg = e.args[0].strip()  # get only msg of exception
        # if err_msg.endswith("for key 'email'\")"):
        if 'Duplicate entry' in err_msg:
            return jsonify({
                "message": f'Email already exists.'
            }), 400

        raise e  # else unrecognized error

    except Exception as e:  # unexpected error
        logger.exception(f'Failed to register {role_name}')
        return f'Internal error: {e}', 500
