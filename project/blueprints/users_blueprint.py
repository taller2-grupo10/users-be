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
        "email": fields.String(required=True, description="User email"),
    },
)


user_response_model = api.inherit(
    "User Response",
    user_model,
    {
        "email": fields.String(required=True, description="User email"),
    },
)


def user_schema(user):
    try:
        email = auth.get_user(user.uid).email
    except:
        email = None
    return {
        "id": user.id,
        "uid": user.uid,
        "artist_id": user.artist_id,
        "roles": [role.id for role in user.roles],
        "permissions": [permission.name for permission in user.permissions],
        "active": user.active,
        "is_deleted": user.is_deleted,
        "created_at": date_to_str(user.created_at) if user.created_at else None,
        "updated_at": date_to_str(user.updated_at) if user.updated_at else None,
        "email": email,
    }


@api.route("")
class Users(Resource):
    # @check_token
    def get(self):
        return [user_schema(user) for user in UserController.load_all()], 200

@api.route("/id/<id>" , doc={"params": {"id": "User id"}})
class Users(Resource):
    # @check_token
    @api.response(200, "Success", user_response_model)
    @api.doc(
        responses={
            200: "{message: User signed up}",
            400: "{message: user_not_found}",
        }
    )
    def get(self, id):
        user = UserController.load_by_id(id)
        if not user: 
          return (
                  {"message": "user_not_found"},
                  400,
            )
        return user_schema(user), 200
    def put(self, id):
      user = UserController.load_updated(id, **request.json)
      return user_schema(user)
