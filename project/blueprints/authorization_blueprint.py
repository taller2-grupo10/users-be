from typing import Dict, List, Tuple
from flask import Blueprint, request, jsonify, current_app
from functools import wraps
from project.models.user import User
from project.blueprints.token_check import check_token

authorization_blueprint = Blueprint("authorization_blueprint", __name__)


@authorization_blueprint.route("/signup", methods=["POST"])
@check_token
def sign_up():
    uid = request.args.get("uid")
    if not uid:
        return {"message": "No uid provided"}, 400
    # user = User(uid=uid)
    # db.session.add(user)
    # db.session.commit()
    return {"message": "User created"}, 201


@authorization_blueprint.route("/login", methods=["POST"])
@check_token
def login():
    uid = request.args.get("uid")
    user = User.query.filter_by(uid=uid).first()
    if not user:
        return {"message": "No user found"}, 400
    return {"message": "User logged in"}, 202
