import os
from pyspark.sql import SparkSession



def set_env_variables(
    path_spark_app='',
    path_mysql_connector_jar='',
    custom=dict(),
):
    """ Sets environment variables to run spark app.
        Returns callable that when called restores them.
    """
    # setup variables revognized by pyspark
    env_vars_new_vals = {
        'SPARK_APPLICATION_PYTHON_LOCATION': path_spark_app,

        'SPARK_SUBMIT_ARGS':
            f'--driver-class-path {path_mysql_connector_jar} --jars {path_mysql_connector_jar}',
        # = f'--driver-class-path /app/mysql-connector-j-8.0.33.jar --jars /app/mysql-connector-j-8.0.33.jar'
    }

    # add custom env vars on top of it
    env_vars_new_vals.update(custom)

    # set the env vars and store vals to restore to
    env_var_old_vals = dict()
    for var, val in env_vars_new_vals.items():
        env_var_old_vals[var], os.environ[var] = os.environ.get(var, ''), val

    def restore_env_variables():
        for var, old_val in env_var_old_vals.items():
            os.environ[var] = old_val

    return restore_env_variables


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
