import os
import subprocess
import sys
from pyspark.sql import SparkSession
from .utils.db_spark_apps import set_env_variables, get_table



class CategoryStatisticsApp:
    @staticmethod
    def main():
        """ Logs to stdout the result of calculating stats.
            Intended to be ran when this file is used in
            separate process by /template.sh file.
        """
        print(CategoryStatisticsApp.compute_stats())

    @staticmethod
    def compute_stats():
        path_mysql_connector_jar = os.environ['MASTER_URL']
        spark_master_url = os.environ['SPARK_MASTER_URL']
        db_store_management_uri = os.environ['DB_STORE_MANAGEMENT_URI']

        builder = SparkSession.builder
        spark: SparkSession = (
            builder.appName('Spark App: CategoryStatisticsApp')
                   .master(spark_master_url)
                   .config('spark.driver.extraClassPath', path_mysql_connector_jar)
                   .getOrCreate()
        )

        products = get_table('products', spark, db_store_management_uri)
        orders = get_table('orders', spark, db_store_management_uri)
        orders_items = get_table('orders_items', spark, db_store_management_uri)

        return products

    def __init__(
        self,
        path_mysql_connector_jar: str,
        spark_cluster_master_url: str,
        db_store_management_uri: str,
        path_spark_app_file: str=None,
    ) -> None:
        """ If path_spark_app_file == None then this module will
            be used a python file to be executed by /template.sh,
            that is if the code is not an exe, if it is a .py
            file path must be provided.
        """
        self._path_mysql_connector_jar = path_mysql_connector_jar
        self._spark_cluster_master_url = spark_cluster_master_url
        self._db_store_management_uri = db_store_management_uri
        self._set_path_spark_app_file(path_spark_app_file)

    def _set_path_spark_app_file(self, path_spark_app_file=None):
        # path_spark_app_file==None => this module as .py file to run,
        # but in case of .exe this module is not a .py file
        if path_spark_app_file is None and getattr(sys, 'frozen', True):
            msg = 'When ran from executable arg `path_spark_app_file` must be provided.'
            raise Exception(msg)

        self._path_spark_app_file = path_spark_app_file \
                                  or os.path.realpath(__file__)

    def calc_stats(self):
        restore_env_variables = set_env_variables(
            path_spark_app=self._path_spark_app_file,
            path_mysql_connector_jar=self._path_mysql_connector_jar,
            custom={
                'SPARK_MASTER_URL': self._spark_cluster_master_url,
                'DB_STORE_MANAGEMENT_URI': self._db_store_management_uri,
            }
        )
        # compute by fetching output of process that runs .py
        # file provided in the os.environ['PATH_SPARK_APPLICATION']
        stats = subprocess.check_output([ '/template.sh' ])
        restore_env_variables()
        return stats



if __name__ == '__main__':
    CategoryStatisticsApp.main()
