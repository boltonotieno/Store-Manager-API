from flask import Flask, Blueprint
from flask_restful import Api
from .views.product_endpoint import Products

version1 = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(version1)

api.add_resource(Products, '/product')