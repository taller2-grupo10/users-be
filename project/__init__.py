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
        namespace as media_artist_namespace,
    )
    from project.blueprints.media_album_blueprint import (
        namespace as media_album_namespace,
    )
    from project.blueprints.media_song_blueprint import (
        namespace as media_song_namespace,
    )
    from project.blueprints.users_blueprint import (
        namespace as users_namespace,
    )
    from project.blueprints.authorization_blueprint import (
        namespace as auth_namespace,
    )

    blueprint = Blueprint("api", __name__, url_prefix="/")

    api_extension = Api(
        blueprint,
        title="Spotifiuby",
        version="0.1",
        description="Documentation of Spotifiuby",
        doc="/doc",
    )

    api_extension.add_namespace(media_artist_namespace)
    api_extension.add_namespace(media_album_namespace)
    api_extension.add_namespace(media_song_namespace)
    api_extension.add_namespace(users_namespace)
    api_extension.add_namespace(auth_namespace)

    app.register_blueprint(blueprint)
