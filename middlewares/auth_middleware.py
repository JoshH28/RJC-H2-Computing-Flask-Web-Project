from functools import wraps
from flask import abort, current_user

def stall_owner_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'stall_owner':
            abort(403)
        return f(*args, **kwargs)
    return decorated