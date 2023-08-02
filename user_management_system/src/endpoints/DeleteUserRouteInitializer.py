from flask import request as flask_request
from flask import jsonify
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt,
)

from sqlalchemy.exc import NoResultFound
from redis import Redis

from ..models import User
from .RouteInitializer import RouteInitializer
from ..decorators import login_required
from .utils import add_jwt_to_blocklist


class DeleteUserRouteInitializer(RouteInitializer):
    def __call__(self, app) -> None:
        """ Init all the user management system endpoints for given app.
        """
        logger = app.app.logger
        db = app.databases["users"]["database"]
        redis: Redis = app['redis_client']

        # ==================================================
        # Endpoints:

        @app.app.route('/delete', methods=["POST"])
        @login_required(reraise=False)
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

                if data['email'] is None:
                    raise ParsingError('Uknown user.')

                return data

            try:
                data = parse_request_data()

                try:
                    user = db.session.query(User) \
                             .filter_by(email=data['email']) \
                             .with_for_update().one()
                    # if user is None:
                    #     raise UserDoesNotExist('Uknown user.')

                    # remove the user and rows that have cascade delete
                    user.delete()

                    # blocklist the token used by this user to access the website                    
                    add_jwt_to_blocklist(redis, get_jwt())

                    db.session.commit()

                except Exception as e:
                    db.session.rollback()
                    raise e

            except ParsingError as e:
                return jsonify({
                    "message": f'{e}'
                }), 400

            except (UserDoesNotExist, NoResultFound) as e:
                msg = 'Unknown user.'
                return jsonify({
                    "message": f'{msg}'
                }), 400

            except Exception as e:  # unexpected error
                logger.exception(f'Failed to delete user')
                return f'Internal error: {e}', 500

            return '', 200
