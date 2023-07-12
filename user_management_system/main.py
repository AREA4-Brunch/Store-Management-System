import pymysql

from src.apps import UserManagementSystem   


pymysql.install_as_MySQLdb()


# ====================================================
# Globals:


APP = UserManagementSystem()


# ====================================================
# RUNNER:


def main():
    APP.run()  # [noreturn]



if __name__ == "__main__":
    main()
