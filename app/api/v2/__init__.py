from flask import Flask, Blueprint
from flask_restful import Api
from .views.registration_endpoint import Registration


version2 = Blueprint('api2', __name__, url_prefix='/api/v2')
api = Api(version2)

api.add_resource(Registration, '/auth/signup')


