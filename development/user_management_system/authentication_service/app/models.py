from .app import get_app


# DB: SQLAlchemy = get_app().container.services.db_user_management()
# MIGRATE: SQLAlchemy = get_app().container.services.migrate_db_user_management()

# get models from db_user_management.models common for the
# whole system and created using SQLAlchemy object properly
# binded in app.py
ALL_MODELS = get_app().container.services.db_user_management_models()


HasRole = ALL_MODELS['HasRole']

User = ALL_MODELS['User']

Role = ALL_MODELS['Role']
