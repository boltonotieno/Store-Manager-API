from flask import Flask, Blueprint
from flask_restful import Api
from .views.registration_endpoint import Registration, User
from .views.login_endpoint import Login


version2 = Blueprint('api2', __name__, url_prefix='/api/v2')
api = Api(version2)

api.add_resource(Registration, '/auth/signup', '/users')
api.add_resource(Login, '/auth/login')
api.add_resource(User, '/users/<int:user_id>')

