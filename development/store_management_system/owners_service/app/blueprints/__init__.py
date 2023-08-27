import flask


ORDERS_BP = flask.Blueprint('orders', __name__)

# Bind the ORDERS_BP endpoints
from . import (
    products_bp
)


STATISTICS_BP = flask.Blueprint('statistics', __name__)

# Bind the STATISTICS_BP endpoints

from . import (
    statistics_bp
)
