from flask import Blueprint, request
from project.blueprints.users_blueprint import user_schema
from project.controllers.user_controller import UserController
from project.helpers.helper_auth import check_token, is_valid_token, check_permissions
from project.helpers.helper_media import MediaRequester
from project.helpers.helper_payments import PaymentRequester
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
        "notification_token": fields.String(
            required=True, description="Notification token provided by Expo"
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
        "location": fields.String(required=True, description="Artist/User location"),
        "genres": fields.List(
            fields.String, required=True, description="Artist/User genres"
        ),
        "notification_token": fields.String(
            required=True, description="User notification token"
        ),
    },
)

login_response_model = api.inherit(
    "Login Response",
    login_model,
    {
        "id": fields.Integer(required=False, description="User id"),
        "uid": fields.String(required=False, description="User identifier"),
        "active": fields.Boolean(required=False, description="User active"),
        "artist_id": fields.String(required=False, description="Artist id"),
        "roles": fields.List(fields.Integer, required=False, description="User roles"),
        "permissions": fields.List(
            fields.String, required=False, description="User permissions"
        ),
        "email": fields.String(required=False, description="User email"),
        "is_deleted": fields.Boolean(required=False, description="User is deleted"),
        "created_at": fields.DateTime(required=False, description="User created at"),
        "updated_at": fields.DateTime(required=False, description="User updated at"),
    },
)


def sign_up(role_id):
    uid = request.json.get("uid")
    name = request.json.get("name")
    notification_token = request.json.get("notification_token")
    location = request.json.get("location")
    genres = request.json.get("genres")
    if not uid or not name or not location or not genres:
        return {"message": "No uid/name/location/genres provided"}, 400
    try:
        user = UserController.load_by_uid(uid)
        if user:
            return {"message": "User already exists"}, 400

        data = {"uid": uid, "name": name, "location": location, "genres": genres}
        response_media, status_code = MediaRequester.post("artists", data)
        response_payment, status_code = PaymentRequester.create_wallet()

        new_user = UserController.create(
            uid=uid,
            role_id=role_id,
            artist_id=response_media["_id"],
            notification_token=notification_token,
            wallet_id=response_payment["id"],
        )
    except ValueError as e:
        print("Error: {}".format(e))
        return {"message": "Error while creating User"}, 400
    return response_media, status_code


@api.route("/login")
class Login(Resource):
    @check_token
    @api.expect(login_model)
    @api.response(200, "Success", login_response_model)
    @api.response(400, "{message: No user found}")
    def post(self):
        notification_token = request.json.get("notification_token")
        user = request.user
        if user.notification_token != notification_token:
            UserController._update(user, notification_token=notification_token)
        return user_schema(user=user), 200


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
        return sign_up(ID_USER)


@api.route("/login/admin")
class AdminLogin(Resource):
    @check_token
    @check_permissions(["admin_login"])
    @api.response(200, "Success", login_response_model)
    def post(self):
        # All the logic is in check_token and check_permissions
        return user_schema(user=request.user), 200


@api.route("/signup/admin")
class AdminSignup(Resource):
    @check_token
    @check_permissions(["admin_creation"])
    @api.expect(signup_model)
    def post(self):
        return sign_up(ID_ADMIN)


@api.route("/signup/superadmin")
class AdminSignup(Resource):
    @check_token
    @check_permissions(["superadmin_creation"])
    @api.expect(signup_model)
    def post(self):
        return sign_up(ID_SUPERADMIN)
