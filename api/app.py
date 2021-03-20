# api/app.py
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy

from api.config import env_config

api = Api()
db = SQLAlchemy()


def create_app(config_name):
    # import our resource folder to avoid circular
    # dependency error
    import resources

    app = Flask(__name__)

    app.config.from_object(env_config[config_name])
    app.config.from_pyfile('config.py')
    api.init_app(app)
    db.init_app(app)

    CORS(app)
    Swagger(app)

    return app
