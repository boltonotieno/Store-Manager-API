from flask import Flask, Blueprint
from flask_restful import Api
from .views.product_endpoint import Products
from .views.sales_endpoint import Sales
from .views.authentication_endpoint import UserRegistration, GetUser, UserLogin


version1 = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(version1)

api.add_resource(Products, '/product', '/product/<int:product_id>')
api.add_resource(Sales, '/sale', '/sale/<int:sale_id>')
api.add_resource(UserRegistration, '/auth/registration', '/users')
api.add_resource(GetUser, '/users/<int:user_id>')
api.add_resource(UserLogin, '/auth/login')
