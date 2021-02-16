"""
I use this module to put utilities
to initialize Flask App.
"""
from flask import Flask
from flask_api import FlaskAPI
from flask_cors import CORS
from flask_jwt_extended import JWTManager


def set_jwt_loaders(jwt_manager):
    """
    This method sets the JWT manager loaders, to allow,
    automatic user loading into Flask's Context
    :param jwt_manager: JWTManger object
    :return: None
    """
    @jwt_manager.user_identity_loader
    def user_identity_lookup(user):
        return user.id

    @jwt_manager.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        # TODO implement
        # return User.query.filter_by(id=identity).one_or_none()


def create_app(**kwargs):
    """
    Initializes flask app.
    :param args:
    :param kwargs:
    :return: FlaskAPI app object.
    """
    from models import DB, migrate
    # Initializing API Flask App.
    app = FlaskAPI("TinyHR")
    # Injecting App configs
    app.config.from_pyfile("config.py", silent=False)
    # Initiating CORS capability
    CORS(app)
    # Initializing DB.
    DB.init_app(app)
    # Initializing JWT authentication.
    jwt = JWTManager(app)
    set_jwt_loaders(jwt)
    # Initialize Migration command
    migrate.init_app(app, DB)
    return app
