from flask import Flask, make_response, jsonify, request
from flask_restful import Api, Resource
from ..models.product import Product
import json

class Products(Resource):
    def post(self):
        data = request.get_json()
        name = data.get('name').strip()
        price = data.get('price').strip()
        quantity = data.get('quantity').strip()
        min_quantity = data.get('min_quantity').strip()
        category = data.get('category').strip()
        
        product_obj= Product(name, price, quantity, min_quantity, category)

        response = jsonify(product_obj.create_product())
        response.status_code = 201

        return response

