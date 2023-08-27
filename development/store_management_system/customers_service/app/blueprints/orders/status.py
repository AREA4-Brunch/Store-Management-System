from . import ORDERS_BP
from flask import (
    request as flask_request,
    current_app,
    jsonify
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload
from std_authentication.decorators import roles_required_login
from std_authentication.services import AuthenticationService
from ...models import Order, OrderItem, Product, ProductCategory



@ORDERS_BP.route('/status', methods=['GET'])
@roles_required_login(
    [ 'customer' ],
    roles_response_func=lambda _: (jsonify({ 'msg': 'Missing Authorization Header' }), 401)
)
def get_order_status():
    db: SQLAlchemy = current_app.container.services.db_store_management()
    logged_in_user_identifier: str \
        = AuthenticationService.get_user_identifier_from_jwt_header()
    logger = current_app.logger

    def get_products_data(price, quantity, id_product):
        product = Product.query.options(
            joinedload(Product.categories)
        ).get(id_product)

        data = {
            'categories': [
                cat.name
                for cat in product.categories
            ],
            'name': product.name,
            'price': price,
            'quantity': quantity,
        }

        return data

    try:
        customer: str = logged_in_user_identifier

        orders = Order.query.filter_by(
            customer=customer
        ).all()

        orders = [
            {
                'products': [
                    get_products_data(item.price,
                                      item.quantity,
                                      item.id_product)
                    for item in order.items
                ],
                'price': order.total_price,
                'status': order.status,
                'timestamp': order.creation_time.isoformat(),
            }
            for order in orders
        ]

        return jsonify({
            'orders': orders
        }), 200


    except Exception as e:  # unexpected error
        logger.exception(f'Failed to get status of customers orders')
        return f'Internal error: {e}', 500
