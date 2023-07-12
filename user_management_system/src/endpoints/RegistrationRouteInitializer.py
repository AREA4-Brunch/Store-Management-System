import re  # for validating email address format

from flask import request as flask_request
from flask import jsonify
from sqlalchemy.exc import IntegrityError

from ..models import User, Role, HasRole
from .RouteInitializer import RouteInitializer
from .utils import is_valid_email_format


class RegistrationRouteInitializer(RouteInitializer):
    def __call__(self, app) -> None:
        """ Init all the user management system endpoints for given app.
        """
        logger = app.app.logger
        db = app.databases["users"]["database"]

        # ==================================================
        # Endpoints:

        @app.app.route('/register_customer', methods=["POST"])
        def register_customer():
            return register_user_view(role_name='customer')

        @app.app.route('/register_courier', methods=["POST"])
        def register_courier():
            return register_user_view(role_name='courier')

        # ==================================================
        # Helpers:

        def register_user_view(role_name):
            class ParsingError(Exception):
                pass

            class ValidationError(Exception):
                pass

            def parse_registration_form():
                data = dict({
                    "forename": flask_request.form.get("forename", ''),
                    "surname": flask_request.form.get("surname", ''),
                    "email": flask_request.form.get("email", ''),
                    "password": flask_request.form.get("password", ''),
                })

                # check if all required fields have been filled out
                def check_missing_fields():
                    for field_name, field_val in data.items():
                        if field_val is None or len(field_val) == 0:
                            raise ParsingError(f'Field {field_name} is missing.')

                check_missing_fields()
                # TODO: check for too long fields, > 256 chars
                return data

            def validate_registration_form(data):
                def validate_email():
                    if not is_valid_email_format(data["email"]):
                        raise ValidationError('Invalid email.')

                def validate_password():
                    if not 8 <= len(data["password"]) <= 256:
                        raise ValidationError('Invalid password.')

                validate_email()
                validate_password()

            try:
                data = parse_registration_form()
                validate_registration_form(data)

                # add the user to the db along with its role
                # with db.session.begin_nested():
                user = User(
                    forename=data["forename"],
                    surname=data["surname"],
                    email=data["email"],
                    password=data["password"]
                )

                db.session.add(user)
                db.session.flush()

                # role = Role.query.filter_by(name=role_name).first()
                role = db.session.query(Role).filter_by(name=role_name) \
                         .with_for_update().one()
                has_role = HasRole(user_id=user.id, role_id=role.id)

                db.session.add(has_role)
                db.session.commit()

            except ParsingError as e:
                return jsonify({
                    "message": f'{e}'
                }), 400

            except ValidationError as e:
                return jsonify({
                    "message": f'{e}'
                }), 400

            except IntegrityError as e:
                err_msg = e.args[0].strip()  # get only msg of exception
                # handle unique fields, tried to set already existing vals
                if 'Duplicate entry' in err_msg:
                    if err_msg.endswith("for key 'email'\")"):
                        return jsonify({
                            "message": f'Email already exists.'
                        }), 400

                raise e  # else unrecognized error

            except Exception as e:  # unexpected error
                logger.exception(f'Failed to register customer')
                return f'Internal error: {e}', 500

            # user successfuly created in db
            return '', 200
