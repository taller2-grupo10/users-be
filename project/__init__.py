from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask import Blueprint
from flask_restx import Api


db = SQLAlchemy()
migrate = Migrate()
cors = CORS()

######################################
#### Application Factory Function ####
######################################


def create_app(config_obj=None):
    app = Flask(__name__)
    app.config.from_object(config_obj)
    register_blueprints(app)
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    return app


def register_blueprints(app):
    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    from project.models.user import User
    from project.models.role import Role
    from project.models.user_role import UserRole

    from project.blueprints.media_artist_blueprint import (
        api as media_artist_namespace,
    )
    from project.blueprints.media_album_blueprint import (
        api as media_album_namespace,
    )
    from project.blueprints.media_song_blueprint import (
        api as media_song_namespace,
    )
    from project.blueprints.users_blueprint import (
        api as users_namespace,
    )
    from project.blueprints.authorization_blueprint import (
        api as auth_namespace,
    )
    from project.blueprints.media_genres_blueprint import (
        api as media_genres_namespace,
    )
    from project.blueprints.media_playlist_blueprint import (
        api as media_playlist_namespace,
    )
    from project.blueprints.media_world_locations_blueprint import (
        api as media_world_locations_namespace,
    )
    from project.blueprints.payments_blueprint import (
        api as payments_namespace,
    )
    from project.blueprints.chat_blueprint import api as chat_namespace
    from project.blueprints.subscriptions_blueprint import (
        api as subscriptions_namespace,
    )
    from project.blueprints.api_token_blueprint import api as api_token_namespace
    from project.blueprints.admin_media_blueprint import (
        api as admin_media_namespace,
    )
    from project.blueprints.media_home_blueprint import (
        api as media_home_namespace,
    )

    blueprint = Blueprint("api", __name__, url_prefix="/")

    api_extension = Api(
        blueprint,
        title="Spotifiuby",
        version="0.1",
        description="Documentation of Spotifiuby Users BE",
        doc="/doc",
    )

    api_extension.add_namespace(media_artist_namespace)
    api_extension.add_namespace(media_album_namespace)
    api_extension.add_namespace(media_song_namespace)
    api_extension.add_namespace(users_namespace)
    api_extension.add_namespace(auth_namespace)
    api_extension.add_namespace(media_genres_namespace)
    api_extension.add_namespace(media_playlist_namespace)
    api_extension.add_namespace(media_world_locations_namespace)
    api_extension.add_namespace(payments_namespace)
    api_extension.add_namespace(chat_namespace)
    api_extension.add_namespace(subscriptions_namespace)
    api_extension.add_namespace(api_token_namespace)
    api_extension.add_namespace(admin_media_namespace)
    api_extension.add_namespace(media_home_namespace)

    app.register_blueprint(blueprint)
