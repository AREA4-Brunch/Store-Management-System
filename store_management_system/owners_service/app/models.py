from .app import get_app


# DB: SQLAlchemy = get_app().container.services.db_store_management()
# MIGRATE: SQLAlchemy = get_app().container.services.migrate_db_store_management()

# get models from db_store_management.models common for the
# whole system and created using SQLAlchemy object properly
# binded in app.py
ALL_MODELS = get_app().container.services.db_store_management_models()


OrderItem = ALL_MODELS['OrderItem']

Order = ALL_MODELS['Order']

IsInCategory = ALL_MODELS['IsInCategory']

ProductCategory = ALL_MODELS['ProductCategory']

Product = ALL_MODELS['Product']
