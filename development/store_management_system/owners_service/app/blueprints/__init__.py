import flask


PRODUCTS_BP = flask.Blueprint('orders', __name__)

# Bind the ORDERS_BP endpoints
from . import (
    add_products
)


STATISTICS_BP = flask.Blueprint('statistics', __name__)

# Bind the STATISTICS_BP endpoints

from . import (
    statistics
)
