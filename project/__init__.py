from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()

######################################
#### Application Factory Function ####
######################################


def create_app(config_filename=None):
    app = Flask(__name__)
    app.config.from_object("project.config.Config")
    db.init_app(app)
    migrate.init_app(app, db)

    return app
