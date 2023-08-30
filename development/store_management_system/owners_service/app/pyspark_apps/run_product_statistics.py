import os
import subprocess
from . import calc_product_statistics as py_spark_app
from ..app import get_app


PATH_FILE_SPARK_APPLICATION = os.path.realpath(py_spark_app.__file__)
PATH_FILE_MYSQL_CONNECTOR_JAR \
    = get_app().container.core.config().pyspark.PATH_FILE_MYSQL_CONNECTOR_JAR



def calc_product_statistics():
    restore_env_variables = set_env_variables()
    out = subprocess.check_output([ '/template.sh' ])
    restore_env_variables()
    return out.decode()


def set_env_variables():
    """ Sets environment variables to run spark app.
        Returns callable that when called restores them.
    """
    env_var_old_vals = dict()
    env_vars_new_vals = {
        'SPARK_APPLICATION_PYTHON_LOCATION': PATH_FILE_SPARK_APPLICATION,

        'SPARK_SUBMIT_ARGS':
            f'--driver-class-path {PATH_FILE_MYSQL_CONNECTOR_JAR} --jars {PATH_FILE_MYSQL_CONNECTOR_JAR}',
        # = f'--driver-class-path /app/mysql-connector-j-8.0.33.jar --jars /app/mysql-connector-j-8.0.33.jar'
    }

    # set the env vars
    for var, val in env_vars_new_vals:
        env_var_old_vals[var], os.environ[var] = os.environ[var], val

    def restore_env_variables():
        for var, old_val in env_var_old_vals:
            os.environ[var] = old_val

    return restore_env_variables
