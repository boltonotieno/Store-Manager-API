from flask import Flask, Blueprint
from flask_restplus import Api
from instance.config import app_config

blue=Blueprint('api', __name__)
api=Api(blue)

# Create the applicatiion
def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
     
    # register Blueprint
    app.register_blueprint(blue,url_prefix='/api/v1')

    return app
