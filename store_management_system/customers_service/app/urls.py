from .blueprints import (
    PRODUCTS_BP,
)


# (url_path_prefix, blueprint_to_bind or iterable of same  structure)
url_blueprints = (
    ('', PRODUCTS_BP),
)
