import os
import subprocess
import sys
from ..utils.db_spark_apps import set_env_variables
from . import computation



class ProductStatisticsApp:
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
        if path_spark_app_file is None and hasattr(sys, 'frozen'):
            msg = 'When ran from executable arg `path_spark_app_file` must be provided.'
            raise Exception(msg)

        self._path_spark_app_file = path_spark_app_file \
                                  or os.path.realpath(computation.__file__)

    def calc_stats(self):
        """ Returns list of json strings. """
        restore_env_variables = set_env_variables(
            path_spark_app=self._path_spark_app_file,
            path_mysql_connector_jar=self._path_mysql_connector_jar,
            custom={  # namespace all custom env vars with PRODUCT_STATISTICS_
                'PRODUCT_STATISTICS_SPARK_MASTER_URL': self._spark_cluster_master_url,
                'PRODUCT_STATISTICS_DB_STORE_MANAGEMENT_URI': self._db_store_management_uri,
            }
        )
        # compute and fetch output of process that runs .py
        # file provided in the os.environ['PATH_SPARK_APPLICATION']
        # sadly gets logs in stdout so extract the response
        stats: str = subprocess.check_output([ '/template.sh' ]) \
                               .decode('utf-8')
        response_delimeter = '~sale~' * 3
        stats = stats[ stats.find(response_delimeter) + len(response_delimeter)
                     : stats.rfind(response_delimeter) ]
        restore_env_variables()
        return stats
