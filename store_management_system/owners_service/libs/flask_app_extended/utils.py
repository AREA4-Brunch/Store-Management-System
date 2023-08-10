import importlib


def load_attr_from_file(attr_path: str):
    """ attr_path = 'path.to.file.attrname' """

    module_name = attr_path[ : attr_path.rfind('.') ]
    attr_name = attr_path[attr_path.rfind('.') + 1 : ]
    attr = getattr(
        importlib.import_module(module_name),
        attr_name
    )
    return attr
