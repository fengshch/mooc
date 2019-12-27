import os

from flask import Flask
from flask_cors import CORS

from .extensions import jwt, db, bcrypt
from .config import config_by_name


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    CORS(app)
    return app


app = create_app(os.getenv('MOOC_ENV') or 'dev')
