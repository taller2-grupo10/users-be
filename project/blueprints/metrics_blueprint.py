"""
CA 1: Métricas de nuevos usuarios utilizando mail y contraseña
CA 2: Métricas de nuevos usuarios utilizando identidad federada

CA 3: Métricas de login de usuarios utilizando mail y contraseña
CA 4: Métricas de login de usuarios utilizando identidad federada

CA 5: Métricas de usuarios bloqueados
CA 6: Métricas de recupero de contraseña
"""


from datetime import datetime, timedelta

from firebase_admin import auth
from flask_restx import Namespace, Resource
from project.helpers.helper_auth import check_token
from project.models.user import User

api = Namespace(name="Metrics", path="metrics", description="Metrics related endpoints")


def is_in_datetime_range(date_time, start, end):
    return (
        start.strftime("%Y-%m-%d %H:%M:%S")
        <= date_time
        <= end.strftime("%Y-%m-%d %H:%M:%S")
    )


def count_new_users(user, from_date, to_date, new_users):
    user_metadata = user.user_metadata
    creation_timestamp = user_metadata.creation_timestamp
    creation_timestamp = datetime.fromtimestamp(
        user_metadata.creation_timestamp / 1000
    ).strftime("%Y-%m-%d %H:%M:%S")

    print("Creation: ", creation_timestamp)

    if not is_in_datetime_range(creation_timestamp, from_date, to_date):
        return
    providers = user.provider_data
    for provider in providers:
        new_users[provider.provider_id] = new_users.get(provider.provider_id, 0) + 1


def count_recent_logins(user, from_date, to_date, logins):
    user_metadata = user.user_metadata
    last_sign_in_timestamp = user_metadata.last_sign_in_timestamp
    last_sign_in_timestamp = datetime.fromtimestamp(
        user_metadata.last_sign_in_timestamp / 1000
    ).strftime("%Y-%m-%d %H:%M:%S")

    print("Sing In:  ", last_sign_in_timestamp)
    if not is_in_datetime_range(last_sign_in_timestamp, from_date, to_date):
        return
    providers = user.provider_data
    for provider in providers:
        logins[provider.provider_id] = logins.get(provider.provider_id, 0) + 1


def count_password_resets(user, from_date, to_date, password_resets):
    user_metadata = user.user_metadata
    last_refresh_timestamp = user_metadata.last_refresh_timestamp
    last_refresh_timestamp = datetime.fromtimestamp(
        user_metadata.last_refresh_timestamp / 1000
    ).strftime("%Y-%m-%d %H:%M:%S")

    print("Refresg:  ", last_refresh_timestamp)
    if not is_in_datetime_range(last_refresh_timestamp, from_date, to_date):
        return
    providers = user.provider_data
    for provider in providers:
        password_resets[provider.provider_id] = (
            password_resets.get(provider.provider_id, 0) + 1
        )


@api.route("/data")
class Data(Resource):
    def get(self):
        from_date = datetime.now() - timedelta(days=2)
        to_date = datetime.now() + timedelta(days=1)

        new_users = {}
        recent_logins = {}
        # password_resets = {}
        blocked = 0

        users = auth.list_users(max_results=1000)

        for user in users.iterate_all():
            print(user.password_salt)
            count_new_users(user, from_date, to_date, new_users)
            count_recent_logins(user, from_date, to_date, recent_logins)
            # count_password_resets(user, from_date, to_date, password_resets)

        for user in User.query.all():
            if not user.active:
                blocked += 1

        print("USERS: ", new_users)
        print("LOGINS: ", recent_logins)
        # print("PASSWORD RESETS: ", password_resets)
        print("BLOCKED: ", blocked)
        return {}, 200
