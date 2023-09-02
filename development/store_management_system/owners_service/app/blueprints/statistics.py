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
        statistics = requests.get(f'{STATISTICS_SERVICE_URL}/product_statistics')
        statistics = statistics.json()
        return jsonify(statistics), 200

    except Exception as e:  # unexpected error
        logger.exception(f'Failed to calc products statistics')
        return f'Internal error: {e}', 500



@STATISTICS_BP.route('/category_statistics', methods=['GET'])
@roles_required_login(
    ['owner'],
    roles_response_func=lambda _: (jsonify({ 'msg': 'Missing Authorization Header' }), 401)
)
def calc_category_statisctics():
    # db: SQLAlchemy = current_app.container.services.db_store_management()
    logger = current_app.logger

    try:
        statistics = requests.get(f'{STATISTICS_SERVICE_URL}/category_statistics')
        statistics = statistics.json()
        return jsonify(statistics), 200

    except Exception as e:  # unexpected error
        logger.exception(f'Failed to calc categorys statistics')
        return f'Internal error: {e}', 500
