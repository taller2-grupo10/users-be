from flask import Blueprint, request
from project.blueprints.auth_helper import check_token
from project.controllers.user_controller import UserController, UserAlreadyExists


authorization_blueprint = Blueprint("authorization_blueprint", __name__)


@authorization_blueprint.route("/signup", methods=["POST"])
@check_token
def sign_up():
    uid = request.json["uid"]
    roles = request.json["roles"]
    if not uid or not roles:
        return {"message": "No uid/roles provided"}, 400
    try:
        UserController.create(uid, roles)
    except (UserAlreadyExists, ValueError) as e:
        return {"message": "Error while creating User"}, 400
    return {"message": "User created"}, 201


@authorization_blueprint.route("/login", methods=["POST"])
@check_token
def login():
    uid = request.json["uid"]
    user = UserController.load_by_uid(uid)
    if not user:
        return {"message": "No user found"}, 400
    return {"message": "User logged in"}, 200
