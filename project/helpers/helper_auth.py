from functools import wraps
from firebase_admin import auth
from flask import request

from project.controllers.user_controller import UserController


def is_valid_token(f):
    """
    Validates that the token is valid.
    """

    @wraps(f)
    def token(*args, **kwargs):
        token = request.headers.get("authorization")
        if token and "Bearer" in token:
            token = token.split()[1]
        else:
            return {"message": "No token provided"}, 400
        try:
            firebase_user = auth.verify_id_token(token)
        except:
            return {"message": "Invalid token provided."}, 400
        return f(*args, **kwargs)

    return token


def check_token(f):
    """
    Validates that the token is valid && the user exists.
    """

    @wraps(f)
    def token(*args, **kwargs):
        token = request.headers.get("authorization")
        if token and "Bearer" in token:
            token = token.split()[1]
        else:
            return {"message": "No token provided"}, 400
        try:
            firebase_user = auth.verify_id_token(token)
            local_user = UserController.load_by_uid(firebase_user["uid"])
            if not local_user:
                return {"message": "No user found"}, 400
            request.user = local_user
        except:
            return {"message": "Invalid token provided."}, 400
        return f(*args, **kwargs)

    return token


def check_permissions(permissions_needed):
    def perms(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user = request.user  # user must exist bc check_token is called first
            permissions = user.permissions

            for permission in permissions_needed:
                if permission not in permissions:
                    return {"message": "User does not have permission"}, 400

            return f(*args, **kwargs)

        return decorated

    return perms
