from .blueprints import (
    USER_ACCOUNT_MANAGEMENT_BP
)


# (url_path_prefix, blueprint_to_bind or iterable of same  structure)
url_blueprints = (
    ('', USER_ACCOUNT_MANAGEMENT_BP),
)
