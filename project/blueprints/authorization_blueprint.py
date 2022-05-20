from flask import Blueprint, request
from project.controllers.user_controller import UserController
from project.helpers.helper_auth import check_token, is_valid_token
from project.helpers.helper_media import MediaRequester
from project.models.user_role import ID_SUPERADMIN, ID_ADMIN, ID_USER
from flask_restx import Namespace, Resource, fields

api = Namespace(
    name="Authorization", path="/auth", description="Authorization related endpoints"
)

login_model = api.model(
    "Login",
    {
        "uid": fields.String(
            required=True, description="User identifier provided by Firebase"
        ),
    },
)

signup_model = api.model(
    "Signup",
    {
        "uid": fields.String(
            required=True, description="User identifier provided by Firebase"
        ),
        "name": fields.String(required=True, description="Artist/User name"),
    },
)

login_response_model = api.inherit(
    "Login Response",
    login_model,
    {
        "id": fields.Integer(required=False, description="User id"),
        "active": fields.Boolean(required=False, description="User active"),
        "artist_id": fields.String(required=False, description="Artist id"),
        "roles": fields.List(fields.Integer, required=False, description="User roles"),
        "permissions": fields.List(
            fields.String, required=False, description="User permissions"
        ),
        "is_deleted": fields.Boolean(required=False, description="User is deleted"),
        "created_at": fields.DateTime(required=False, description="User created at"),
        "updated_at": fields.DateTime(required=False, description="User updated at"),
    },
)


@api.route("/login")
class Login(Resource):
    @check_token
    @api.expect(login_model)
    @api.response(200, "Success", login_response_model)
    @api.response(400, "{message: No user found}")
    def post(self):
        uid = request.json["uid"]
        user = UserController.load_by_uid(uid)
        if not user:
            return {"message": "No user found"}, 400
        return {
            "id": user.id,
            "uid": user.uid,
            # "active": user.active,
            "artist_id": user.artist_id,
            # "roles": [role.id for role in user.roles],
            # "permissions": user.permissions,
            # "is_deleted": user.is_deleted,
            # "created_at": user.created_at,
            # "updated_at": user.updated_at,
        }, 200


@api.route("/signup")
class Signup(Resource):
    @is_valid_token
    @api.expect(signup_model)
    @api.doc(
        responses={
            200: "{message: User signed up}",
            400: "{message: User already exists || No uid/name provided || Error while creating User}",
        }
    )
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
