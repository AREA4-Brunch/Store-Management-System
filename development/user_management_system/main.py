import pymysql

from src.settings import Settings
from src.apps import UserManagementSystem   


# pymysql.install_as_MySQLdb()


# ====================================================
# Globals:


APP = UserManagementSystem()


# ====================================================
# RUNNER:


def main():
    APP.run(
        host=Settings.HOST,
        port=Settings.PORT
    )  # [noreturn]



if __name__ == "__main__":
    main()
