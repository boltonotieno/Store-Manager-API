from flask import Flask, Blueprint
from instance.config import app_config
from flask_jwt_extended import JWTManager


# Create the applicatiion
def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SECRET_KEY'] = 'the-secret-secret'
    app.config['JWT_SECRET_KEY'] = 'secret'
    jwt=JWTManager(app)

    @jwt.user_claims_loader
    def add_claims_to_access_token(user_object):
        '''add role claims to access token'''
        return {'role': user_object['role']}

    @jwt.user_identity_loader
    def user_identity_lookup(user_object):
        '''set token identity from user_object passed to username'''
        print(user_object)
        return user_object["username"]

    

    # register Blueprint
    from .api.v1 import version1 as v1
    app.register_blueprint(v1)

    return app
