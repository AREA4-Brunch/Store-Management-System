import flask


PRODUCT_STATS_BP = flask.Blueprint('product_stats', __name__)
from . import (  # bind view funcs to blueprint
    product_statistics,
)


CATEGORY_STATS_BP = flask.Blueprint('categories_stats', __name__)
from . import (  # bind view funcs to blueprint
    category_statistics,
)


def register_endpoints(app: flask.Flask):
    app.register_blueprint(PRODUCT_STATS_BP, url_prefix='')
    app.register_blueprint(CATEGORY_STATS_BP, url_prefix='')
