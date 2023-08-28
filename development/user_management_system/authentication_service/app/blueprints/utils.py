import re
from datetime import datetime
from redis import Redis
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    verify_jwt_in_request
)
from std_authentication.utils import get_expiry_hour


def is_valid_email_format(email):
    # pattern = r'[\w]+(?:[\.\-_]?[^\.\-\_])*@[\w]+(?:[\.\-_]?[^\.\-\_])*$'
    pattern = r'[\w]+(?:[\.\-_]?[^\.\-\_])*@[\w]+\.[\w]{2,}$'
    regex = re.compile(pattern)
    return re.fullmatch(regex, email)


def generate_jwts(user):
    claims = {
        # 'email': user.email,  # identity
        'forename': user.forename,
        'surname': user.surname,
        "roles": [ role.name for role in user.roles ]
    }

    access_token = create_access_token(
        identity=user.email,  # user.id better ?
        additional_claims=claims
    )
    
    refresh_token = create_refresh_token(
        identity=user.email,
        additional_claims=claims
    )

    return access_token, refresh_token, claims


def is_logged_in():
    """ Returns pair (is_logged_in: bool, exception_caught: Exception).
    """
    try:
        verify_jwt_in_request()
        return True, None

    except Exception as e:
        return False, e


def add_jwt_to_blocklist(redis: Redis, jwt_payload: dict):
    jti = jwt_payload['jti']
    expiry_hour, time_format = get_expiry_hour(jwt_payload)
    blocklist_group = f'jwt_blk:exp={expiry_hour}'
    redis.sadd(blocklist_group, jti)

    # if this is the 1st el of set add expiry time to the set
    if not redis.ttl(blocklist_group):
        expiry_hour_as_datetime = datetime.strptime(expiry_hour,
                                                    time_format)
        # time till the end of the hour in which jwt expires
        group_ttl = int((expiry_hour_as_datetime - datetime.now())\
                        .total_seconds())
        redis.expire(blocklist_group, group_ttl)
