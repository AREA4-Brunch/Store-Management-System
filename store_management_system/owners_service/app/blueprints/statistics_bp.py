import csv
from flask import (
    Blueprint,
    request as flask_request,
    current_app,
    jsonify,
)
from flask_sqlalchemy import SQLAlchemy
from std_authentication.decorators import roles_required_login
from ..models import Order, Product



STATISTICS_BP = Blueprint('statistics', __name__)


# @STATISTICS_BP.route('/product_statistics', methods=['GET'])
# @roles_required_login(['owner'])
# def calc_product_statisctics():
#     # db: SQLAlchemy = current_app.container.services.db_store_management()
#     logger = current_app.logger

#     try:
#         statistics = []

#         # find all products that have been sold
#         products = Product.query.filter(
#             Product.orders.any(Order.status=='DELIVERED')
#         ).all()

#         for product in products:
#             waiting_cnt = product.orders.query.filter(
#                 Order.status=='SHIPPING'
#             ).count()

#             # delivered == all - shipping
#             sold_cnt = product.orders.count() - waiting_cnt

#             statistics.append({
#                 'name': product.name,
#                 'sold': sold_cnt,
#                 'waiting': waiting_cnt,
#             })

#         return jsonify({
#             'statistics': statistics
#         }), 200

#     except Exception as e:  # unexpected error
#         logger.exception(f'Failed to calc products statistics')
#         return f'Internal error: {e}', 500


# @STATISTICS_BP.route('/category_statistics', methods=['GET'])
# @roles_required_login(['owner'])
# def calc_category_statistics():
#     # db: SQLAlchemy = current_app.container.services.db_store_management()
#     logger = current_app.logger
#     try:
#         statistics = []

#         return jsonify({
#             'statistics': statistics
#         }), 200

#     except Exception as e:  # unexpected error
#         logger.exception(f'Failed to calc categories statistics')
#         return f'Internal error: {e}', 500
