from flask_restful import Resource, reqparse
import psycopg2
from flask import jsonify
from ..models.product_model import Products
from ..models import db_connection

#passing incoming data into post requests
parser = reqparse.RequestParser()
parser.add_argument('name', help = 'This field cannot be blank', required = True)
parser.add_argument('price', help = 'This field cannot be blank', required = True)
parser.add_argument('quantity', help = 'This field cannot be blank', required = True)
parser.add_argument('min_quantity', help = 'This field cannot be blank', required = True)
parser.add_argument('category', help = 'This field cannot be blank', required = True)

class Product(Resource):

    def post(self):
        """Post new products"""
        connection = db_connection()
        cursor = connection.cursor()

        data = parser.parse_args()
        name = data['name']
        price = data['price']
        quantity = data['quantity']
        min_quantity = data['min_quantity']
        category = data['category']
        
        new_product = Products()
        sql = new_product.create_product()
        cursor.execute(sql,(name,price,quantity,min_quantity,category))
        connection.commit()
        
        return {
                'message': 'Product created successfully',
            },201

  