import os
import logging
from flask_migrate import init, migrate, upgrade



def update_db_structure():
    def init_if_not_already():
        if os.path.isdir('./migrations'):
            return

        try:
            init()

        except Exception as e:
            logging.exception(f'Failed to run flask-migrate\'s init: {e}')

    init_if_not_already()

    try:
        migrate(message='Initial Production Migration; user_management_db_init')

    except Exception as e:
        logging.exception(f'Failed to run flask-migrate\'s migrate: {e}')
        raise e

    try:
        upgrade()

    except Exception as e:
        logging.exception(f'Failed to run flask-migrate\'s upgrade: {e}')
        raise e
