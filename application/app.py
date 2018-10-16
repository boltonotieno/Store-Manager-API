from flask import Blueprint
from flask_restful import Api
from flask_api import FlaskAPI
from instance.config import app_config

blue = Blueprint('api', __name__)
api = Api(blue)

# Create our application
def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    
    # register Blueprint
    app.register_blueprint(blue, url_prefix='/api/v1')

    return app
