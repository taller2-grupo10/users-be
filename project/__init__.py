from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()

######################################
#### Application Factory Function ####
######################################


def create_app(config_obj=None):
    app = Flask(__name__)
    app.config.from_object(config_obj)
    register_blueprints(app)
    db.init_app(app)
    migrate.init_app(app, db)

    return app


def register_blueprints(app):
    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    from project.models.user import User
    from project.models.role import Role
    from project.models.user_role import UserRole

    from project.blueprints.authorization_blueprint import authorization_blueprint

    app.register_blueprint(authorization_blueprint)
