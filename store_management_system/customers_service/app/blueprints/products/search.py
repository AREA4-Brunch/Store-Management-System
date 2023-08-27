from flask import (
    request as flask_request,
    current_app,
    jsonify,
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload
from std_authentication.decorators import roles_required_login
from ...models import Product, ProductCategory
from . import PRODUCTS_BP


@PRODUCTS_BP.route('/search', methods=['GET'])
@roles_required_login(
    ['customer'],
    roles_response_func=lambda _: (jsonify({ 'msg': 'Missing Authorization Header' }), 401)
)
def search_products_and_categories():
    # db: SQLAlchemy = current_app.container.services.db_store_management()
    logger = current_app.logger

    def fetch_fields():
        form_fields = dict({
            'product_name': flask_request.args.get('name', ''),
            'category_name': flask_request.args.get('category', ''),
        })

        return form_fields

    def search(product_name, category_name):
        # fetch categories names and ids (for later search)
        categories = ProductCategory.query.filter(
            ProductCategory.name.contains(category_name),
            ProductCategory.products.any(
                Product.name.contains(product_name),
            )
        ).with_entities(
            ProductCategory.id, ProductCategory.name
        ).all()

        categories_ids = [ id for (id, name) in categories ]
        categories = [ name for (id, name) in categories ]

        products = Product.query.filter(
            Product.name.contains(product_name),
            Product.categories.any(
                ProductCategory.id.in_(categories_ids)
            ),
        ).options(
            joinedload(Product.categories)
        ).all()

        products = [
            {
                'categories': [ cat.name for cat in product.categories ],
                'id': product.id,
                'name': product.name,
                'price': product.price
            } for product in products
        ]

        return categories, products

    try:
        form_fields = fetch_fields()
        categories, products = search(
            form_fields['product_name'],
            form_fields['category_name']
        )

        return jsonify({
            'categories': categories,
            'products': products
        }), 200  # successfully queried

    except Exception as e:  # unexpected error
        logger.exception(f'Failed to search products and categories')
        return f'Internal error: {e}', 500
