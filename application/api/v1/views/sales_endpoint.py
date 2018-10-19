from flask import Flask, make_response, jsonify, request
from flask_restful import Api, Resource
from ..models.sales_model import Sale
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, 
jwt_refresh_token_required, jwt_required, get_jwt_identity, get_raw_jwt)


class Sales(Resource):
    """This class contain methods for sales endpoints"""
    @jwt_required
    def post(self):
        """This method handles post requsts to create new sales"""
        data = request.get_json()
        name = data.get('name').strip()
        price = data.get('price').strip()
        quantity = data.get('quantity').strip()

        single_sale = Sale()
        
        response = jsonify(single_sale.create_sale(name, price, quantity))
        response.status_code = 201

        return response

    def get(self, sale_id=None):
        """This method handles get requests to fetch all sales"""
        if sale_id is None:   
            sale_objs = Sale()
            response = jsonify(sale_objs.get_all_sale())
            response.status_code = 200

            return response
        
        sale_obj = Sale()

        response = jsonify(sale_obj.get_one_sale(sale_id))
        response.status_code = 200
        
        return response

