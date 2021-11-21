from flask import request, Response


def preflight_request_handler(main_method):
    def decorator(method):
        def wrapper():
            if request.method == 'OPTIONS':
                response = Response()
                response.access_control_allow_origin = '*'
                response.access_control_allow_methods = ['OPTIONS', main_method]
                return response
            else:
                return method()
        wrapper.__name__ = method.__name__
        return wrapper
    return decorator
