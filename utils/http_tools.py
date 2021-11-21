from flask import make_response


def http_response(data):

    response = make_response(data)
    response.access_control_allow_origin = "*"
    return response
