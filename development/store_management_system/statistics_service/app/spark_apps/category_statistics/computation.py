import os
import logging
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import when, sum, desc, asc


RESPONSE_DELIMETER = '~sale~' * 3
LOG_FILE_PATH = f'./logs/category_statistics.log'
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
        json_stats: str = compute_stats(logger)
        print(f'{RESPONSE_DELIMETER}{json_stats}{RESPONSE_DELIMETER}')

    except Exception as e:
        logger.exception(f'Products Statistics App computation failure:\n\n{e}')
        print(e)


def compute_stats(logger):
    """ Computes category statistics and returns the result
        as json string.
    """
    spark_master_url = os.environ['CATEGORY_STATISTICS_SPARK_MASTER_URL']
    db_store_management_uri = os.environ['CATEGORY_STATISTICS_DB_STORE_MANAGEMENT_URI']

    builder = SparkSession.builder
    spark: SparkSession = (
        builder.appName('Spark App: ProductStatisticsApp')
               .master(spark_master_url)
               .config('spark.driver.extraClassPath', 'mysql-connector-j-8.0.33.jar')
               .config('spark.log.level', 'ERROR')
               .config('spark.log.dir', '/app/logs/spark2.log')
               .getOrCreate()
    )

    try:
        spark.sparkContext.setLogLevel('ERROR')

        categories = get_table('product_categories', spark, db_store_management_uri)
        products = get_table('products', spark, db_store_management_uri)
        is_in_category = get_table('is_in_category', spark, db_store_management_uri)
        orders_items = get_table('orders_items', spark, db_store_management_uri)
        orders = get_table('orders', spark, db_store_management_uri)

        orders_items = categories.join(
            is_in_category,
            is_in_category['id_product_category'] == categories['id'],
            'left'
        ).join(
            products,
            is_in_category['id_product'] == products['id'],
            'left'
        ).join(
            orders_items,
            orders_items['id_product'] == products['id'],
            'left'
        ).join(
            orders,
            orders['id'] == orders_items['id_order'],
            'left'
        ).groupBy(
            categories['name']
        ).agg(
            sum(
                when(
                    orders['status'] == 'COMPLETE',
                    orders_items['quantity']
                ).otherwise(0)
            ).alias('completed_cnt')
        ).orderBy(
            desc('completed_cnt'),
            asc(categories['name'])
        ).select(
            categories['name']
        ).collect()

        # for row in orders_items:
        #     logger.error(f'Row: {row}')

        orders_items = [ row['name'] for row in orders_items ]
        orders_items = json.dumps(orders_items)
        return orders_items

    except Exception as e:
        raise e

    finally:
        spark.stop()


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

    logger = logging.getLogger('category.statistics')
    logger.addHandler(file_handler)

    return logger



if __name__ == '__main__':
    main()
