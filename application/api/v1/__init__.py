from flask import Flask, Blueprint
from flask_restful import Api
from .views.product_endpoint import Products
from .views.sale_endpoint import Sales


version1 = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(version1)

api.add_resource(Products, '/product', '/product/<int:product_id>')
api.add_resource(Sales, '/sale', '/sale/<int:sale_id>')
