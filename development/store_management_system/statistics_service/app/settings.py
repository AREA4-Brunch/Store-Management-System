import os
import logging
from flask import Flask
from .__secrets import STORE_MANAGEMENT_DB  # in production to replace with env variables



DB_STORE_MANAGEMENT_URI = os.environ.get(
    'DB_STORE_MANAGEMENT_URI',
    f"mysql+pymysql://root:{STORE_MANAGEMENT_DB['pwd']}@localhost:3306/store_management"
)

LOG_LEVEL = getattr(logging, os.environ.get('LOGGING_LEVEL', 'DEBUG'))



def init_logger(
    app: Flask,
    log_file_path: str=r'./logs/log1.log',
    log_level=LOG_LEVEL,
):
    format = r'%(asctime)s [%(levelname)s] %(message)s'
    datefmt = '%Y-%m-%d %H:%M:%S'

    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(log_level)
    formatter = logging.Formatter(format, datefmt=datefmt)
    file_handler.setFormatter(formatter)

    app.logger.addHandler(file_handler)
    return app.logger
