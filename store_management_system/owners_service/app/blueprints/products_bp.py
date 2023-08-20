from flask import Blueprint, jsonify
from libs.authentication.decorators import login_required


PRODUCTS_BP = Blueprint('products', __name__)


@PRODUCTS_BP.route('/update', methods=['POST'])
@login_required()
def add_products_batch():
    return 'Hello Worlds!', 200
