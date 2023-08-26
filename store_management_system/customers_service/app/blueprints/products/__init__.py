import flask


PRODUCTS_BP = flask.Blueprint('products', __name__)


# Bind the blueprint function to blueprint object
from . import (
    search
)
