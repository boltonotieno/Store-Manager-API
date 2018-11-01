from flask import Flask, Blueprint
from instance.config import app_config
from flask_jwt_extended import JWTManager
from .api.v2.models.user_model import Users
from app.api.v2.models import create_tables, create_default_admin
from app.api.v2.views.login_endpoint import TOKEN_BLACKLIST

# Create the applicatiion
def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    create_tables()
    create_default_admin()
    app.url_map.strict_slashes = False
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SECRET_KEY'] = 'the-secret-secret'
    app.config['JWT_SECRET_KEY'] = 'secret'
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']

    jwt=JWTManager(app)

    @jwt.token_in_blacklist_loader
    def check_if_token_blacklist(decrypted_token):
        """checks if jti(unique identifier) is in the token blacklist set"""
        jti = decrypted_token['jti']
        return jti in TOKEN_BLACKLIST

    # register Blueprint
    from .api.v1 import version1 as v1
    app.register_blueprint(v1)

    from .api.v2 import version2 as v2
    app.register_blueprint(v2)

    return app
