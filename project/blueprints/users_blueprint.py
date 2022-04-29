from flask import Blueprint, jsonify, request
from project.blueprints.token_check import check_token
from project.controllers.user_controller import UserController
from firebase_admin import auth

users_blueprint = Blueprint("users_blueprint", __name__)
USERS_ENDPOINTS = "/users"


def user_schema(user):
    try:
        email = (auth.get_user(user.uid).email,)
    except:
        email = None
    return {
        "id": user.id,
        "uid": user.uid,
        "roles": [role.id for role in user.roles],
        "is_deleted": user.is_deleted,
        "created_at": user.created_at,
        "updated_at": user.updated_at,
        "email": email,
    }


@users_blueprint.route(f"{USERS_ENDPOINTS}", methods=["GET"])
@check_token
def get_all_users():
    return jsonify([user_schema(user) for user in UserController.load_all()]), 200
