from firebase_admin import auth
from flask import Blueprint, jsonify
from project.controllers.user_controller import UserController
from project.helpers.helper_auth import check_token
from project.helpers.helper_date import date_to_str
from project.helpers.helper_media import MediaRequester
from flask_restx import Namespace, Resource, fields


api = Namespace(
    name="Users", path="/admin/users", description="Users related endpoints"
)


def user_schema(user):
    try:
        email = auth.get_user(user.uid).email
    except:
        email = None
    return {
        "id": user.id,
        "uid": user.uid,
        "roles": [role.id for role in user.roles],
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
