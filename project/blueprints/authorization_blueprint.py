from flask import Blueprint, request
from project.controllers.user_controller import UserController
from project.helpers.helper_auth import check_token, is_valid_token
from project.helpers.helper_media import MediaRequester
from project.models.user_role import ID_SUPERADMIN, ID_ADMIN, ID_USER
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
    @is_valid_token
    def post(self):
        uid = request.json["uid"]
        name = request.json["name"]
        if not uid or not name:
            return {"message": "No uid/name provided"}, 400
        try:
            user = UserController.load_by_uid(uid)
            if user:
                return {"message": "User already exists"}, 400

            data = {"uid": uid, "name": name}
            response, status_code = MediaRequester.post("artists", data)
            new_user = UserController.create(
                uid=uid, role_id=ID_USER, artist_id=response["_id"]
            )
        except ValueError as e:
            return {"message": "Error while creating User"}, 400
        return response, status_code


