from flask import Flask, Blueprint
from instance.config import app_config
from flask_jwt_extended import JWTManager
from .api.v2.models.user_model import Users


# Create the applicatiion
def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SECRET_KEY'] = 'the-secret-secret'
    app.config['JWT_SECRET_KEY'] = 'secret'
    jwt=JWTManager(app)

    # register Blueprint
    from .api.v1 import version1 as v1
    app.register_blueprint(v1)

    from .api.v2 import version2 as v2
    app.register_blueprint(v2)

    return app
