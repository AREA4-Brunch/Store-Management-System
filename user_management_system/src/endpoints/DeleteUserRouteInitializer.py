from flask import request as flask_request
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt


from ..models import User
from .RouteInitializer import RouteInitializer
from ..decorators import login_required


class DeleteUserRouteInitializer(RouteInitializer):
    def __call__(self, app) -> None:
        """ Init all the user management system endpoints for given app.
        """
        logger = app.app.logger
        db = app.databases["users"]["database"]

        # ==================================================
        # Endpoints:

        @app.app.route('/delete', methods=["POST"])
        @login_required(reraise=True)
        def delete_user():
            return delete_user_view()

        # ==================================================
        # Helpers:

        def delete_user_view():
            class UserDoesNotExist(Exception):
                pass

            class ParsingError(Exception):
                pass

            def parse_request_data():
                data = dict({
                    'email': get_jwt_identity(),
                    # 'additional_claims': get_jwt()
                })

                return data

            try:
                data = parse_request_data()

                with db.session.begin():
                    user = db.session.query(User).with_for_update() \
                            .filter_by(email=data['email']).one()

                    if user is None:
                        raise UserDoesNotExist('Uknown user.')

                    # remove the user and rows that have cascade delete
                    user.delete()
                    db.session.commit()

            except ParsingError as e:
                return jsonify({
                    "message": f'{e}'
                }), 400

            except UserDoesNotExist as e:
                return jsonify({
                    "message": f'{e}'
                }), 400

            except Exception as e:  # unexpected error
                logger.exception(f'Failed to delete user')
                return f'Internal error: {e}', 500

            return '', 200
