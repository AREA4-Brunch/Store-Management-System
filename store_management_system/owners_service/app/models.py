from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from .app import get_app



DB: SQLAlchemy = get_app().container.services.db_store_management()
# MIGRATE: SQLAlchemy = get_app().container.services.migrate_db_store_management()



class ContainsOrderProduct(DB.Model):
    __tablename__ = 'contains_orders_products'

    id = DB.Column(DB.Integer, primary_key=True)
    id_product = DB.Column(DB.Integer, DB.ForeignKey('products.id'), nullable=False)
    id_order = DB.Column(DB.Integer, DB.ForeignKey('orders.id'), nullable=False)


class Order(DB.Model):
    __tablename__ = 'orders'

    id = DB.Column(DB.Integer, primary_key=True)
    total_price = DB.Column(DB.Float, nullable=False)
    status = DB.Column(DB.String(16), nullable=False)
    creation_time = DB.Column(DB.DateTime(timezone=True), nullable=False, default=datetime.now())

    products = DB.relationship(
        'Product',
        secondary=ContainsOrderProduct.__table__,
        back_populates='orders'
    )


class ProductCategory(DB.Model):
    __tablename__ = 'product_categories'

    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(128), nullable=False, unique=True)


class Product(DB.Model):
    __tablename__ = 'products'

    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(128), nullable=False, unique=True)
    price = DB.Column(DB.Float, nullable=False)

    orders = DB.relationship(
        'Order',
        secondary=ContainsOrderProduct.__table__,
        back_populates='products'
    )


class Delivering(DB.Model):
    __tablename__ = 'delivering'

    id = DB.Column(DB.Integer, DB.ForeignKey('orders.id'), primary_key=True, nullable=False)
    # foreign key ???
    id_customer = DB.Column(DB.Integer, nullable=False)
