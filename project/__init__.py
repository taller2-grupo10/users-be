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
    db.init_app(app)
    migrate.init_app(app, db)

    return app
