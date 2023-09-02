import json
from flask import (
    current_app,
    jsonify,
)
from . import PRODUCT_STATS_BP
from ..spark_apps.product_statistics.app import ProductStatisticsApp



@PRODUCT_STATS_BP.route('/product_statistics', methods=['GET', 'POST'])
def product_statistics():
    product_stats_app: ProductStatisticsApp \
        = current_app.container.product_statistics()
    logger = current_app.logger

    try:
        statistics = json.loads(product_stats_app.calc_stats())
        # statistics = product_stats_app.calc_stats()

        return jsonify({
            "statistics": [ json.loads(row) for row in statistics ]
        }), 200

    except Exception as e:  # unexpected error
        logger.exception(f'Failed to calc products statistics')
        return f'Internal error: {e}', 500
