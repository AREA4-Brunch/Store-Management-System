import re


def is_valid_email_format(email):
    pattern = r'[\w]+(?:[\.\-_]?[^\.\-\_])*@[\w]+(?:[\.\-_]?[^\.\-\_])*'
    regex = re.compile(pattern)
    return re.fullmatch(regex, email)
