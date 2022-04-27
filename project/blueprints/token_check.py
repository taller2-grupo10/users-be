from functools import wraps
from firebase_admin import auth
from flask import request


def check_token(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        token = request.headers.get("authorization")
        if token and "Bearer" in token:
            token = token.split()[1]
        else:
            return {"message": "No token provided"}, 400
        try:
            user = auth.verify_id_token(token)
            request.user = user
        except:
            return {"message": "Invalid token provided."}, 400
        return f(*args, **kwargs)

    return wrap
