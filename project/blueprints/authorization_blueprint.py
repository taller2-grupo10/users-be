from flask import Blueprint, request
from project.controllers.user_controller import UserAlreadyExists, UserController
from project.helpers.helper_auth import check_token
from project.helpers.helper_media import MediaRequester
from flask_restx import Namespace, Resource, fields

namespace = Namespace(
    name="Authorization", path="auth", description="Authorization related endpoints"
)


@namespace.route("/login")
class Login(Resource):
    @check_token
    def post(self):
        uid = request.json["uid"]
        user = UserController.load_by_uid(uid)
        if not user:
            return {"message": "No user found"}, 400
        return {"message": "User logged in"}, 200


@namespace.route("/signup")
class Signup(Resource):
    @check_token
    def post(self):
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
