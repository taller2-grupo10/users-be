from flask import Blueprint, request
from project.controllers.user_controller import UserAlreadyExists, UserController
from project.helpers.helper_auth import check_token
from project.helpers.helper_media import MediaRequester

authorization_blueprint = Blueprint("authorization_blueprint", __name__)


@authorization_blueprint.route("/signup", methods=["POST"])
@check_token
def sign_up():
    uid = request.json["uid"]
    roles = request.json["roles"]
    name = request.json["name"]
    if not uid or not roles:
        return {"message": "No uid/roles provided"}, 400
    try:
        UserController.create(uid, roles)
        data = {"userId": uid, "name": name}
        MediaRequester.post("artists", data)
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
