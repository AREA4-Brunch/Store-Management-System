from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
# from .app import get_app


# db: SQLAlchemy = get_app().container.services.db_store_management()
# MIGRATE: SQLAlchemy = get_app().container.services.migrate_db_store_management()


def create_models(db: SQLAlchemy) -> dict:
    class OrderItem(db.Model):
        __tablename__ = 'orders_items'

        id = db.Column(db.Integer, primary_key=True)
        id_product = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
        id_order = db.Column(db.BigInteger, db.ForeignKey('orders.id'), nullable=False)
        quantity = db.Column(db.Integer, nullable=False)
        price = db.Column(db.Float, nullable=False)


    class Order(db.Model):
        __tablename__ = 'orders'

        id = db.Column(db.BigInteger, primary_key=True)
        total_price = db.Column(db.Float, nullable=False)
        # status values: (CREATED, PENDING, COMPLETE)
        status = db.Column(db.String(16), nullable=False)
        creation_time = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.now())
        customer = db.Column(db.String(256), nullable=False)
        contract_address = db.Column(db.String(256), default='')

        items = db.relationship(
            'OrderItem',
            backref='order',  # OrderItem.order
            lazy='dynamic'
        )


    class IsInCategory(db.Model):
        __tablename__ = 'is_in_category'

        id = db.Column(db.Integer, primary_key=True)
        id_product = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
        id_product_category = db.Column(db.Integer, db.ForeignKey('product_categories.id'), nullable=False)


    class ProductCategory(db.Model):
        __tablename__ = 'product_categories'

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(128), nullable=False, unique=True)

        products = db.relationship(
            'Product',
            secondary=IsInCategory.__table__,
            back_populates='categories',  # Product.categories
            cascade=''
        )


    class Product(db.Model):
        __tablename__ = 'products'

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(128), nullable=False, unique=True)
        price = db.Column(db.Float, nullable=False)

        categories = db.relationship(
            'ProductCategory',
            secondary=IsInCategory.__table__,
            back_populates='products',  # ProductCategory.products
            cascade=''
        )


    # add all classes that should be returned and group them
    # in dictionary by their own name
    classes = [
        OrderItem,
        Order,
        IsInCategory,
        ProductCategory,
        Product,
    ]

    # return each class under its own name in dict
    classes_dict = dict()

    for class_ in classes:
        classes_dict[class_.__name__] = class_

    return classes_dict
