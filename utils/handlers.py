from flask import request, Response


def preflight_request_handler(method):
    def wrapper():
        response = Response()
        response.access_control_allow_origin = '*'
        if request.method == 'OPTIONS':
            response.access_control_allow_methods = ['OPTIONS', 'GET', 'POST']
            response.access_control_allow_headers = ['CurrentUserLogin', 'AuthToken', 'Accept', 'Accept-Encoding', 'Content-Type', 'Origin']
            response.access_control_max_age = '86400'
        else:
            response.response = method()
        return response
    wrapper.__name__ = method.__name__
    return wrapper
