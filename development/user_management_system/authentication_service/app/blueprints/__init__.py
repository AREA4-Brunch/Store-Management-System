import flask


USER_ACCOUNT_MANAGEMENT_BP = flask.Blueprint('user_account_management', __name__)


# register view functions to the blueprint
from .login import login_user
from .register import (
    register_courier,
    register_customer
)
from .delete import delete_user
