import flask


ORDERS_BP = flask.Blueprint('orders', __name__)

# Bind the blueprint function to blueprint object
from . import (
    orders_to_deliver,
    pick_up_order
)
