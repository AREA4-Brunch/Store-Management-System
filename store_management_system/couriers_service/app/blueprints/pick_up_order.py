from flask import (
    request as flask_request,
    current_app,
    jsonify,
)
from flask_sqlalchemy import SQLAlchemy
from std_authentication.decorators import roles_required_login
from . import ORDERS_BP
from ..models import Order



@ORDERS_BP.route('/pick_up_order', methods=['POST'])
@roles_required_login(
    ['courier'],
    roles_response_func=lambda _: (jsonify({ 'msg': 'Missing Authorization Header' }), 401)
)
def pick_up_order():
    db: SQLAlchemy = current_app.container.services.db_store_management()
    logger = current_app.logger

    class FieldMissingError(Exception):
        pass

    class ParsingError(Exception):
        pass

    class ValidationError(Exception):
        pass

    def get_id():
        id = flask_request.json.get('id', None)
        if id is None:
            raise FieldMissingError(f'Missing order id.')

        try:  # convert to int
            id = int(id)
        except Exception:
            raise ParsingError(f'Invalid order id.')

        if id <= 0:
            raise ValidationError(f'Invalid order id.')

        return id

    def get_order(id: int):
        order = Order.query.filter_by(id=id).first()

        if order is None:  # order does not exist
            raise ValidationError(f'Invalid order id.')

        # check if the order has not been picked or deliverd
        # up by any courier yet
        if order.status != 'CREATED':
            raise ValidationError(f'Invalid order id.')

        return order

    try:
        # TODO: check if this user is allowed to change the order
        id = get_id()
        order = get_order(id)

        try:
            order.status = 'PENDING'
            db.session.add(order)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            raise e

        return '', 200

    except (FieldMissingError, ParsingError, ValidationError) as e:
        return jsonify({
            'message': f'{e}'
        }), 400

    except Exception as e:  # unexpected error
        logger.exception(f'Failed to set the order\'s status `COMPLETE`.')
        return f'Internal error: {e}', 500
