from .app import get_app


ALL_MODELS = get_app().container.services.db_store_management_models()


OrderItem = ALL_MODELS['OrderItem']

Order = ALL_MODELS['Order']

IsInCategory = ALL_MODELS['IsInCategory']

ProductCategory = ALL_MODELS['ProductCategory']

Product = ALL_MODELS['Product']
