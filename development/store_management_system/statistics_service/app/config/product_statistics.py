import os


from ..settings import (
    DB_STORE_MANAGEMENT_URI,
)

from .common import (
    PATH_MYSQL_CONNECTOR_JAR,
)

PATH_SPARK_APP_PY = os.environ.get(
    'PATH_PRODUCT_STATISTICS_SPARK_APP_PY',
    None  # src code will consider itself .py file to execute
)

SPARK_MASTER_URL = os.environ.get(
    'PRODUCT_STATISTICS_SPARK_MASTER_URL',
    'spark://spark-master:7077'
)
