from functools import wraps
from flask import abort
from flask_login import current_user

def plot_access_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        plot_access = getattr(current_user, 'plot_access', False)
        if not plot_access:
            abort(401)
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        admin = getattr(current_user, 'admin', False)
        if not admin:
            abort(401)
        return f(*args, **kwargs)
    return decorated_function