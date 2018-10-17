from flask import Flask, make_response, jsonify, request
from flask_restful import Api, Resource
from ..models.sales_model import Sale
import json

class Sales(Resource):
    """This class contain methods for sales endpoints"""
    def post(self):
        """This method handles post requsts to create new sales"""
        data = request.get_json()
        name = data.get('name').strip()
        quantity = data.get('quantity').strip()

        single_sale = Sale(name, quantity)
        
        response = jsonify(single_sale.create_sale())
        response.status_code = 201

        return response

