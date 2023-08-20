from flask_sqlalchemy import SQLAlchemy
from .app import get_app


DB: SQLAlchemy = get_app().container.services.db_store_management()
# MIGRATE: SQLAlchemy = get_app().container.services.migrate_db_store_management()



