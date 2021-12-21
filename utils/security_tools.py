from secrets import token_urlsafe


def get_auth_token():

    return token_urlsafe(32)
