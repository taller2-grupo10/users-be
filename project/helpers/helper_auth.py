from functools import wraps
from firebase_admin import auth
from flask import request

from project.controllers.user_controller import UserController


def check_token(f):
    @wraps(f)
    def token(*args, **kwargs):
        token = request.headers.get("authorization")
        if token and "Bearer" in token:
            token = token.split()[1]
        else:
            return {"message": "No token provided"}, 400
        try:
            user = auth.verify_id_token(token)
            uid = request.json["uid"]
            if uid != user["uid"]:
                return {"message": "Uid does not match"}, 400
            request.user = user
        except:
            return {"message": "Invalid token provided."}, 400
        return f(*args, **kwargs)

    return token


def check_permissions(permissions_needed):
    def perms(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            try:
                uid = request.user["uid"]
                user = UserController.load_by_uid(uid)
                permissions = user.permissions

                for permission in permissions_needed:
                    if permission not in permissions:
                        return {"message": "User does not have permission"}, 400
            except:
                return {"message": "User not found"}, 400
            return f(*args, **kwargs)

        return decorated

    return perms
