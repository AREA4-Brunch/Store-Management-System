from pyspark.sql import SparkSession
from ..app import get_app


MASTER_URL = get_app().container.core.config().pyspark.MASTER_URL
PATH_FILE_MYSQL_CONNECTOR_JAR \
    = get_app().container.core.config().pyspark.PATH_FILE_MYSQL_CONNECTOR_JAR


def main():
    builder = SparkSession.builder.appName(f'Spark App: {__file__}')
    spark = builder.master(MASTER_URL) \
                   .config('spark.driver.extraClassPath',
                           PATH_FILE_MYSQL_CONNECTOR_JAR) \
                   .getOrCreate()

    


if __name__ == '__main__':
    main()
