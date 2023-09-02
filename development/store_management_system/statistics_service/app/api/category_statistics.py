import json
from flask import (
    current_app,
    jsonify,
)
from . import CATEGORY_STATS_BP
from ..spark_apps.category_statistics.app import CategoryStatisticsApp



@CATEGORY_STATS_BP.route('/category_statistics', methods=['GET', 'POST'])
def category_statistics():
    category_stats_app: CategoryStatisticsApp \
        = current_app.container.category_statistics()
    logger = current_app.logger

    try:
        statistics = json.loads(category_stats_app.calc_stats())

        return jsonify({
            "statistics": statistics
        }), 200

    except Exception as e:  # unexpected error
        logger.exception(f'Failed to calc categorys statistics')
        return f'Internal error: {e}', 500
