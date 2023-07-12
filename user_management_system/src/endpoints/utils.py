import re
from flask_jwt_extended import create_access_token, create_refresh_token


def is_valid_email_format(email):
    pattern = r'[\w]+(?:[\.\-_]?[^\.\-\_])*@[\w]+(?:[\.\-_]?[^\.\-\_])*'
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
