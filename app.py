import os
from flask import Flask, jsonify
from flask_smorest import Api
from flask_migrate import Migrate
from dotenv import load_dotenv

from db import db
import models

from resources.company import blp as CompanyBlueprint
from resources.user import blp as UserBlueprint
from resources.photo import blp as PhotoBlueprint
from resources.recognition import blp as RecognitionBlueprint


def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "FA REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URI", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate = Migrate(app, db)

    api = Api(app)

    with app.app_context():
        api.register_blueprint(CompanyBlueprint)
        api.register_blueprint(UserBlueprint)
        api.register_blueprint(PhotoBlueprint)
        api.register_blueprint(RecognitionBlueprint)

    return app
