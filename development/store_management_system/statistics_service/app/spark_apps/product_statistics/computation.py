import os
import logging
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import when, sum


RESPONSE_DELIMETER = '~sale~' * 3
LOG_FILE_PATH = f'/logs/product_statistics.log'
LOG_LEVEL = logging.DEBUG



def main():
    """ Logs to stdout the result of calculating stats within
        a delimeter: '~sale~' * 3 beacuse pyspark logging keeps
        logging to stdout.
        Intended to be ran when this file is used in
        separate process by `/template.sh` file.
    """
    # logging.disable(logging.CRITICAL)
    logging.getLogger('org.apache.spark').setLevel('ERROR')
    logging.getLogger('py4j').setLevel('ERROR')
    logger = create_logger()

    try:
        json_stats: str = compute_stats()
        print(f'{RESPONSE_DELIMETER}{json_stats}{RESPONSE_DELIMETER}')

    except Exception as e:
        logger.exception(f'Products Statistics App computation failure:\n\n{e}')
        print(e)


def compute_stats():
    """ Computes product statistics and returns the result
        as json string.
    """
    # path_mysql_connector_jar = os.environ['PATH_MYSQL_CONNECTOR_JAR']
    spark_master_url = os.environ['SPARK_MASTER_URL']
    db_store_management_uri = os.environ['DB_STORE_MANAGEMENT_URI']

    builder = SparkSession.builder
    spark: SparkSession = (
        builder.appName('Spark App: ProductStatisticsApp')
               .master(spark_master_url)
               .config('spark.driver.extraClassPath', 'mysql-connector-j-8.0.33.jar')
               .config('spark.log.level', 'ERROR')
               .config('spark.log.dir', '/app/logs/spark1.log')
               .getOrCreate()
    )
    spark.sparkContext.setLogLevel('ERROR')

    products = get_table('products', spark, db_store_management_uri)
    orders = get_table('orders', spark, db_store_management_uri)
    orders_items = get_table('orders_items', spark, db_store_management_uri)

    # store results in orders_items as the table
    # likely takes most space
    orders_items = products.join(
        orders_items,
        orders_items['id_product'] == products['id']
    ).join(
        orders,
        orders['id'] == orders_items['id_order']
    ).groupBy(
        # products['id'],  # if 2 products have same name
        products['name']
    ).agg(
        sum(
            when(
                orders['status'] == 'COMPLETE',
                orders_items['quantity']
            ).otherwise(0)
        ).alias('sold'),
        sum(
            when(
                orders['status'] != 'COMPLETE',
                orders_items['quantity']
            ).otherwise(0)
        ).alias('waiting'),
    ).toJSON().collect()

    orders_items = json.dumps(orders_items)

    # orders_items = [
    #     json.dumps(21),
    #     json.dumps("Hello Worlds!")
    # ]

    # orders_items = json.dumps(orders_items)

    spark.stop()
    return orders_items


def get_table(table_name: str, spark: SparkSession, db_uri: str):
    db_name = db_uri.split("/")[-1]

    table_df = (
        spark.read
             .format('jdbc')
             .option('driver', 'com.mysql.cj.jdbc.Driver')
             .option('url', f'jdbc:{db_uri}')
             .option('dbtable', f'{db_name}.{table_name}')
             .load()
    )

    return table_df


def create_logger():
    format = r'%(asctime)s [%(levelname)s] %(message)s'
    datefmt = '%Y-%m-%d %H:%M:%S'

    file_handler = logging.FileHandler(LOG_FILE_PATH)
    file_handler.setLevel(LOG_LEVEL)
    formatter = logging.Formatter(format, datefmt=datefmt)
    file_handler.setFormatter(formatter)

    logger = logging.getLogger('product.statistics')
    logger.addHandler(file_handler)

    return logger



if __name__ == '__main__':
    main()
