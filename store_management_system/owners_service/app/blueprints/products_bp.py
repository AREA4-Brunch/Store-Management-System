from flask import Blueprint


PRODUCTS_BP = Blueprint('products', __name__)


@PRODUCTS_BP.route('/update', methods=['POST'])
def add_products_batch():
    return 'Hello Worlds!'
