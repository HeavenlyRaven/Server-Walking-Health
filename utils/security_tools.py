def get_auth_token():

    with open("AUTH_TOKEN.txt", 'r') as token_file:
        token = token_file.read()

    return token
