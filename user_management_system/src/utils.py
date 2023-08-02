from datetime import datetime, timedelta


def get_expiry_hour(jwt_payload: dict):
    """ Returns time by which the given jwt will have expired,
        and the format in which the time is returned.
    """
    time_format = "%Y-%m-%dT%H"
    expires = jwt_payload['exp']
    expiry_hour = datetime.fromtimestamp(expires) + timedelta(hours=1)
    expiry_hour = expiry_hour.strftime(time_format)
    return expiry_hour, time_format
