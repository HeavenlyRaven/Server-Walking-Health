from flask import request, Response, json


def preflight_request_handler(method):
    def wrapper():
        response = Response()
        response.access_control_allow_origin = '*'
        if request.method == 'OPTIONS':
            response.access_control_allow_methods = ['OPTIONS', 'GET', 'POST']
            response.access_control_allow_headers = ['CurrentUserLogin', 'AuthToken', 'Accept', 'Accept-Encoding', 'Content-Type', 'Origin']
            response.access_control_max_age = '86400'
        else:
            response.content_type = "application/json"
            response.data = json.dumps(method())
        return response
    wrapper.__name__ = method.__name__
    return wrapper
