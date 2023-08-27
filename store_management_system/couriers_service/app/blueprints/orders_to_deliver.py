from flask import (
    current_app,
    jsonify,
)
from flask_sqlalchemy import SQLAlchemy
from std_authentication.decorators import roles_required_login
from . import ORDERS_BP
from ..models import Order



@ORDERS_BP.route('/orders_to_deliver', methods=['GET'])
@roles_required_login(
    ['courier'],
    roles_response_func=lambda _: (jsonify({ 'msg': 'Missing Authorization Header' }), 401)
)
def get_orders_to_deliver():
    # db: SQLAlchemy = current_app.container.services.db_store_management()
    logger = current_app.logger

    try:
        # TODO: check if this user is allowed to see the orders

        orders = Order.query.filter_by(
            status='CREATED'
        ).with_entities(
            Order.id,
            Order.customer,
        ).all()

        orders = [
            {
                'id': order[0],
                'email': order[1]
            }
            for order in orders
        ]

        return jsonify({
            'orders': orders
        }), 200  # successfully queried for orders

    except Exception as e:  # unexpected error
        logger.exception(f'Failed to get orders with status `CREATED`.')
        return f'Internal error: {e}', 500
