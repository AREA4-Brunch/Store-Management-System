from redis import Redis
from flask import (
    # request as flask_request,
    current_app,
    jsonify,
)
from flask_jwt_extended import (
    get_jwt_identity,
    get_jwt,
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound
from std_authentication.decorators import (
    login_required,
)
from . import USER_ACCOUNT_MANAGEMENT_BP
from ..models import User
from .utils import add_jwt_to_blocklist



@USER_ACCOUNT_MANAGEMENT_BP.route('/delete', methods=['POST'])
@login_required()
def delete_user():
    db: SQLAlchemy = current_app.container.services.db_user_management()
    redis_client: Redis = current_app.container.gateways.redis_client_auth()
    logger = current_app.logger

    class ParsingError(Exception):
        pass

    class UserDoesNotExist(Exception):
        pass

    def parse_request_data():
        data = dict({
            'email': get_jwt_identity(),
            # 'additional_claims': get_jwt()
        })

        if data['email'] is None:
            raise Exception('Email not in header, how did user pass @login_required ?')

        return data

    try:
        data = parse_request_data()

        try:
            user = User.query.filter_by(email=data['email']) \
                       .with_for_update().one()
            # if user is None: raise UserDoesNotExist('Uknown user.');

        except NoResultFound:
            raise UserDoesNotExist('Uknown user.')

        try:
            # remove the user and rows that have cascade delete
            user.delete()

            # blocklist the token used by this user to access the website                    
            add_jwt_to_blocklist(redis_client, get_jwt())

            db.session.commit()

        except Exception as e:
            db.session.rollback()
            raise e

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
