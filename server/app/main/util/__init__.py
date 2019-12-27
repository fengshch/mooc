from functools import wraps

from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims


def system_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if 'system' not in claims['roles']:
            return {
                'message': '对不起, 你没有系统管理员权限!'
            }, 403
        else:
            return fn(*args, **kwargs)
    return wrapper


def manager_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if 'manager' not in claims['roles']:
            return {
                       'message': '对不起, 你没有课程管理员权限!'
                   }, 403
        else:
            return fn(*args, **kwargs)
    return wrapper
