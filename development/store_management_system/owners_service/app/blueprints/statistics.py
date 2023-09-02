import requests
import json
from flask import (
    # request as flask_request,
    current_app,
    jsonify,
)
# from flask_sqlalchemy import SQLAlchemy
from std_authentication.decorators import roles_required_login
from . import STATISTICS_BP
from ..app import get_app


STATISTICS_SERVICE_URL = get_app().container.gateways.config().statistics.SERVICE_URL




@STATISTICS_BP.route('/product_statistics', methods=['GET'])
@roles_required_login(
    ['owner'],
    roles_response_func=lambda _: (jsonify({ 'msg': 'Missing Authorization Header' }), 401)
)
def calc_product_statisctics():
    # db: SQLAlchemy = current_app.container.services.db_store_management()
    logger = current_app.logger

    try:
        # receive json object as a string
        statistics = requests.get(f'{STATISTICS_SERVICE_URL}/product_statistics')
        logger.info(f'\nRECIEVED RESPONSE:{statistics}')
        logger.info(f'\nRECIEVED CONTENT:{statistics.content}')
        statistics = statistics.json()
        logger.info(f'\nRECIEVED AS JSON:{statistics}')
        # statistics = statistics.json()
        return jsonify(statistics), 200

    except Exception as e:  # unexpected error
        logger.exception(f'Failed to calc products statistics')
        return f'Internal error: {e}', 500


# @STATISTICS_BP.route('/category_statistics', methods=['GET'])
# @roles_required_login(
#     ['owner'],
#     roles_response_func=lambda _: (jsonify({ 'msg': 'Missing Authorization Header' }), 401)
# )
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
