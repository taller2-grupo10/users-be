from firebase_admin import auth
from flask import Blueprint, jsonify, request
from project.controllers.user_controller import UserController
from project.helpers.helper_auth import check_token
from project.helpers.helper_date import date_to_str
from project.helpers.helper_media import MediaRequester
from flask_restx import Namespace, Resource, fields


api = Namespace(
    name="Users", path="/admin/users", description="Users related endpoints"
)

user_model = api.model(
    "User",
    {
        "active": fields.Boolean(required=False, description="User system status"),
        "email": fields.String(required=False, description="User email"),
        "artist_id": fields.String(required=False, description="User artist id"),
        "createdAt": fields.DateTime(required=False, description="User created at"),
        "id": fields.String(required=True, description="User id"),
        "permissions": fields.List(
            fields.String, required=False, description="User permissions"
        ),
        "roles": fields.List(fields.Integer, required=False, description="User roles"),
        "uid": fields.String(required=False, description="User firebase uid"),
        "updatedAt": fields.DateTime(required=False, description="User updated at"),
        "notificationToken": fields.String(
            required=False, description="User notification token"
        ),
        "name": fields.String(required=False, description="User name"),
        "location": fields.String(required=False, description="User location"),
        "genres": fields.List(fields.String, required=False, description="User genres"),
    },
)

user_response_model = api.inherit("User Response", user_model)


user_put_response_model = api.model(
    "User Put Response",
    {
        "code": fields.String(
            required=True,
            description="User updated",
            example="user_updated",
        ),
        "data": fields.Nested(user_response_model),
    },
)


def user_schema(user):
    try:
        artist_data, status_code = MediaRequester.get(f"artists/{user.artist_id}")
        if status_code != 200:
            artist_data = None
        email = auth.get_user(user.uid).email
    except:
        artist_data = None
        email = None
    return {
        "id": user.id,
        "uid": user.uid,
        "artist_id": user.artist_id,
        "roles": [role.id for role in user.roles],
        "permissions": [permission for permission in user.permissions],
        "active": user.active,
        "is_deleted": user.is_deleted,
        "created_at": date_to_str(user.created_at) if user.created_at else None,
        "updated_at": date_to_str(user.updated_at) if user.updated_at else None,
        "email": email,
        "notification_token": user.notification_token,
        "name": artist_data.get("name") if artist_data else None,
        "location": artist_data.get("location") if artist_data else None,
        "genres": artist_data.get("genres") if artist_data else None,
    }


@api.route("")
class Users(Resource):
    @check_token
    @api.response(
        200,
        "Success",
        fields.List(
            fields.Nested(
                user_response_model, required=False, description="List of users"
            )
        ),
    )
    def get(self):
        return [user_schema(user) for user in UserController.load_all()], 200


@api.route("/id/<id>", doc={"params": {"id": "User id"}})
class User(Resource):
    @check_token
    @api.response(200, "Success", user_response_model)
    @api.doc(responses={404: "{code: NO_USER_FOUND}"})
    def get(self, id):
        user = UserController.load_by_id(id)
        if not user:
            return (
                {"code": "NO_USER_FOUND"},
                404,
            )
        return user_schema(user), 200

    @api.expect(user_model)
    @api.response(200, "Success", user_put_response_model)
    @api.doc(responses={404: "{code: NO_USER_FOUND}"})
    def put(self, id):
        user = UserController.load_updated(id, **request.json)
        if not user:
            return (
                {"code": "NO_USER_FOUND"},
                404,
            )

        return (
            {
                "code": "USER_UPDATED",
                "data": user_schema(user),
            },
            200,
        )
