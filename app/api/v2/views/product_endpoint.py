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

    def get(self):
        """Get all Products"""

        connection = db_connection()
        cursor = connection.cursor()

        products = Products()
        sql = products.get_all_products()
        cursor.execute(sql)
        data = cursor.fetchall()

        if data is None:
            return {'message' : 'No products'}

        return {
                'message' : 'success',
                'Users' : data
            },200

class SingleProduct(Resource):
    def get(self, product_id):
        """Get one Product"""

        connection = db_connection()
        cursor = connection.cursor()

        product = Products()
        sql = product.get_one_product()
        cursor.execute(sql,(product_id,))
        data = cursor.fetchone()

        if data is None:
            return {'message' : 'Product not Found'}

        return {
            'message' : 'success',
            'User' : data
        },200

    def put(self, product_id):
        """Modify one Product"""

        connection = db_connection()
        cursor = connection.cursor()

        data = parser.parse_args()
        name = data['name']
        price = data['price']
        quantity = data['quantity']
        min_quantity = data['min_quantity']
        category = data['category']

        product = Products()
        sql = product.modify_product()
        cursor.execute(sql,(name,price,quantity,min_quantity,category,product_id,))
        connection.commit()

        return {
                'message': 'successfuly modified',
            },201


        
