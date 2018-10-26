from flask import Flask, Blueprint
from flask_restful import Api
from .views.registration_endpoint import Registration, User
from .views.login_endpoint import Login
from .views.product_endpoint import Product, SingleProduct
from .views.category_endpoint import Category, SingleCategory


version2 = Blueprint('api2', __name__, url_prefix='/api/v2')
api = Api(version2)

api.add_resource(Registration, '/auth/signup', '/users')
api.add_resource(Login, '/auth/login')
api.add_resource(User, '/users/<int:user_id>')
api.add_resource(Product, '/products')
api.add_resource(SingleProduct, '/products/<int:product_id>')
api.add_resource(Category, '/category')
api.add_resource(SingleCategory, '/category/<int:category_id>')

