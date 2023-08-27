from typing import Type
from flask import (
    request as flask_request,
)


def flask_request_get_typechecked(
    flask_request_attr: str,
    type: Type,
    *flask_req_args,
):
    """ Calls flask.request.flask_request_attr.get.(*flask_req_args).
        Returns value returned by get if it is an instance of
        given type `type`,
        else returns None.
    """
    get = getattr(flask_request, flask_request_attr).get
    res = get(*flask_req_args)
    return res if isinstance(res, type) else None
