import csv
from flask import (
    # request as flask_request,
    current_app,
    jsonify,
)
# from flask_sqlalchemy import SQLAlchemy
from std_authentication.decorators import roles_required_login
from . import STATISTICS_BP
from ..pyspark_apps.run_product_statistics import calc_product_statistics




@STATISTICS_BP.route('/product_statistics', methods=['GET'])
@roles_required_login(
    ['owner'],
    roles_response_func=lambda _: (jsonify({ 'msg': 'Missing Authorization Header' }), 401)
)
def calc_product_statisctics():
    # db: SQLAlchemy = current_app.container.services.db_store_management()
    logger = current_app.logger

    try:
        statistics = calc_product_statistics()

        return jsonify({
            'statistics': statistics
        }), 200

    except Exception as e:  # unexpected error
        logger.exception(f'Failed to calc products statistics')
        return f'Internal error: {e}', 500


@STATISTICS_BP.route('/category_statistics', methods=['GET'])
@roles_required_login(
    ['owner'],
    roles_response_func=lambda _: (jsonify({ 'msg': 'Missing Authorization Header' }), 401)
)
def calc_category_statistics():
    # db: SQLAlchemy = current_app.container.services.db_store_management()
    logger = current_app.logger

    try:
        statistics = []

        return jsonify({
            'statistics': statistics
        }), 200

    except Exception as e:  # unexpected error
        logger.exception(f'Failed to calc categories statistics')
        return f'Internal error: {e}', 500
