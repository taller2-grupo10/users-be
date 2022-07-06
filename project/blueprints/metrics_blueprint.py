"""
CA 1: Métricas de nuevos usuarios utilizando mail y contraseña
CA 2: Métricas de nuevos usuarios utilizando identidad federada

CA 3: Métricas de login de usuarios utilizando mail y contraseña
CA 4: Métricas de login de usuarios utilizando identidad federada

CA 5: Métricas de usuarios bloqueados
CA 6: Métricas de recupero de contraseña
"""


from datetime import datetime

import pytz
from firebase_admin import auth
from flask import request
from flask_restx import Namespace, Resource
from project.helpers.helper_auth import check_token
from project.models.password_reset_request import PasswordResetRequest
from project.models.user import User

utc = pytz.UTC

api = Namespace(name="Metrics", path="metrics", description="Metrics related endpoints")


def is_in_datetime_range(date_time, start):
    return start.strftime("%Y-%m-%d %H:%M:%S") <= date_time


def count_new_users(user, from_date, new_users):
    user_metadata = user.user_metadata
    creation_timestamp = user_metadata.creation_timestamp
    creation_timestamp = datetime.fromtimestamp(
        user_metadata.creation_timestamp / 1000
    ).strftime("%Y-%m-%d %H:%M:%S")

    if not is_in_datetime_range(creation_timestamp, from_date):
        return
    providers = user.provider_data
    for provider in providers:
        new_users[provider.provider_id] = new_users.get(provider.provider_id, 0) + 1


def count_recent_logins(user, from_date, logins):
    user_metadata = user.user_metadata
    last_sign_in_timestamp = user_metadata.last_sign_in_timestamp
    last_sign_in_timestamp = datetime.fromtimestamp(
        user_metadata.last_sign_in_timestamp / 1000
    ).strftime("%Y-%m-%d %H:%M:%S")

    if not is_in_datetime_range(last_sign_in_timestamp, from_date):
        return
    providers = user.provider_data
    for provider in providers:
        logins[provider.provider_id] = logins.get(provider.provider_id, 0) + 1


def count_blocked_users():
    blocked = 0
    for user in User.query.all():
        if not user.active:
            blocked += 1
    return blocked


def count_password_reset_requests(from_date):
    password_resets = 0
    for password_reset_request in PasswordResetRequest.query.all():
        if password_reset_request.created_at.replace(tzinfo=utc) > from_date.replace(
            tzinfo=utc
        ):
            password_resets += 1
    return password_resets


@api.route("/data")
class Data(Resource):
    @check_token
    def get(self):
        from_date = datetime.strptime(request.args.get("from_date"), "%d/%m/%Y")

        new_users = {}
        recent_logins = {}
        password_resets = count_password_reset_requests(from_date)
        blocked = count_blocked_users()

        users = auth.list_users(max_results=1000)

        for user in users.iterate_all():
            count_new_users(user, from_date, new_users)
            count_recent_logins(user, from_date, recent_logins)

        return {
            "new_users": new_users,
            "recent_logins": recent_logins,
            "password_resets": password_resets,
            "blocked": blocked,
        }, 200
