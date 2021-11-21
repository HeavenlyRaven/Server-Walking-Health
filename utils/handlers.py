from flask import request, Response


def preflight_request_handler(method):
    def wrapper():
        if request.method == 'OPTIONS':
            response = Response()
            response.access_control_allow_origin = '*'
            response.access_control_allow_methods = ['OPTIONS', 'GET', 'POST']
            response.access_control_allow_headers = ['CurrentUserLogin', 'AuthToken']
            response.access_control_max_age = '86400'
            return response
        else:
            return method()
    wrapper.__name__ = method.__name__
    return wrapper
