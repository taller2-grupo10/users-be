from flask import jsonify, request
from flask_restx import Namespace, Resource, fields
from project.blueprints.users_blueprint import user_schema
from project.controllers.user_controller import UserController
from project.helpers.helper_auth import check_permissions, check_token, is_valid_token
from project.helpers.helper_logger import Logger
from project.helpers.helper_media import MediaRequester
from project.helpers.helper_payments import PaymentRequester
from project.models.password_reset_request import PasswordResetRequest
from project.models.user_role import ID_ADMIN, ID_USER

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
        Logger.info(
            f"Signup: Missing required fields: uid->{uid}, name->{name}, location->{location}, genres->{genres}"
        )
        return {"code": "MISSING_SIGN_UP_PARAMETERS"}, 400
    try:
        user = UserController.load_by_uid(uid)
        if user:
            Logger.info(f"Signup: User already exists, uid: {uid}")
            return {"code": "EXISTING_USER"}, 400

        data = {"uid": uid, "name": name, "location": location, "genres": genres}

        response_media, status_code = MediaRequester.post("artists", data)
        if status_code != 201:
            Logger.error(f"Signup: Error while creating artist, uid: {uid}")
            return {"code": "FAILED_TO_CREATE_USER"}, 400

        response_payment, status_code = PaymentRequester.create_wallet()
        if status_code != 201:
            Logger.error(f"Signup: Error creating wallet, uid: {uid}")
            return {"code": "FAILED_TO_CREATE_USER"}, 400

        new_user = UserController.create(
            uid=uid,
            role_id=role_id,
            artist_id=response_media["_id"],
            notification_token=notification_token,
            wallet_id=response_payment["id"],
        )
        if not new_user:
            Logger.error(f"Signup: Failed to create user, uid: {uid}")
            return {"code": "FAILED_TO_CREATE_USER"}, 400
    except ValueError as e:
        return {"code": "FAILED_TO_CREATE_USER"}, 400
    return user_schema(new_user), 201


@api.route("/login")
class Login(Resource):
    @check_token
    @api.expect(login_model)
    @api.response(200, "Success", login_response_model)
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
    @api.response(200, "Success", login_response_model)
    @api.doc(
        responses={
            400: "{code: MISSING_SIGN_UP_PARAMETERS || EXISTING_USER || FAILED_TO_CREATE_USER}",
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
    @api.response(200, "Success", login_response_model)
    @api.doc(
        responses={
            400: "{code: MISSING_SIGN_UP_PARAMETERS || EXISTING_USER || FAILED_TO_CREATE_USER}",
        }
    )
    def post(self):
        return sign_up(ID_ADMIN)


@api.route("/loggedIn", methods=["GET"])
class IsLoggedIn(Resource):
    @check_token
    @api.response(200, "Success")
    def get(self):
        """
        Endpoint to check if user is still logged in.
        Used to render pages in front-end.
        If user is not logged in, "Invalid token provided" answer is returned by @check_token.
        """
        return {"code": "LOGGED_IN"}, 200


@api.route("/passwordReset/<email>", methods=["POST"])
class PasswordReset(Resource):
    # @api.response(200, "Success")
    def post(self, email):
        """
        Endpoint to send password reset email.
        """
        password_reset = PasswordResetRequest(email)
        password_reset.save()
        return {"code": "PASSWORD_RESET_EMAIL_SENT"}, 200
