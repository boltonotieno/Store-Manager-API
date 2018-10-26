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
        
        try:
            new_product = Products()
            sql = new_product.create_product()
            cursor.execute(sql,(name,price,quantity,min_quantity,category))
            connection.commit()
            
            return {
                    'message': 'Product created successfully',
                },201
        except:
            return {'message' : 'Product already exist'}

    def get(self):
        """Get all Products"""

        connection = db_connection()
        cursor = connection.cursor()

        products = Products()
        sql = products.get_all_products()
        cursor.execute(sql)
        data = cursor.fetchall()

        if len(data) == 0:
            return {'message' : 'No products'}

        return {
                'message' : 'success',
                'Products' : data
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
            'Product' : data
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

        try:
            product = Products()
            sql = product.modify_product()
            cursor.execute(sql,(name,price,quantity,min_quantity,category,product_id))
            connection.commit()

            return {
                    'message': 'successfuly modified'
                },200
        except:
            return {'message': 'Product already exist'}

    def delete(self, product_id):
        """delete one Product"""

        connection = db_connection()
        cursor = connection.cursor()

        try:
            product = Products()
            sql = product.delete_product()
            cursor.execute(sql,(product_id,))
            connection.commit()

            return {
                    'message': 'successfuly deleted'
                },200
        except:
            return {'message' : 'Product not found'}

        
