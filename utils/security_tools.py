from os import path


def get_auth_token():

    with open(path.join(path.dirname(__file__), "AUTH_TOKEN.txt"), 'r') as token_file:
        token = token_file.read()

    return token
