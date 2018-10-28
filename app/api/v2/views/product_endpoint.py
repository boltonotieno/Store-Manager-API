from flask_restful import Resource, reqparse
import psycopg2
from flask import jsonify
from ..models.product_model import Products
from ..models.user_model import Users
from ..models import db_connection
from flask_jwt_extended import (create_access_token, jwt_required, get_jwt_claims, get_jwt_identity)

#passing incoming data into post requests
parser = reqparse.RequestParser()
parser.add_argument('name', help = 'This field cannot be blank', required = True)
parser.add_argument('price', help = 'This field cannot be blank', required = True)
parser.add_argument('quantity', help = 'This field cannot be blank', required = True)
parser.add_argument('min_quantity', help = 'This field cannot be blank', required = True)
parser.add_argument('category', help = 'This field cannot be blank', required = True)

connection = db_connection()
cursor = connection.cursor()

class Product(Resource):
    @jwt_required
    def post(self):
        """Post new products: only by the admin"""

        role = Users().get_user_role()

        if role[0] != "admin":
            return {
                "message" : "Access not allowed"
            },403

        data = parser.parse_args()
        name = data['name']
        price = data['price']
        quantity = data['quantity']
        min_quantity = data['min_quantity']
        category = data['category']

        if name.isalpha() == False:
            return {'message' : 'Invalid product name'},400

        if price.isdigit() == False:
            return {'message' : 'Invalid product price'},400
        
        if quantity.isdigit() == False:
            return {'message' : 'Invalid product quantity'},400

        if min_quantity.isdigit() == False:
            return {'message' : 'Invalid product minimum quantity'},400

        if category.isalpha() == False:
            return {'message' : 'Invalid product category'},400

        try:
            new_product = Products()
            sql = new_product.create_product()
            cursor.execute(sql,(name,price,quantity,min_quantity,category))
            connection.commit()
            
            return {
                    'message': 'Product created successfully'
                },201
        except:
            return {'message' : 'Product {} already exist'.format(name)},409

    @jwt_required
    def get(self):
        """Get all Products"""

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
    @jwt_required
    def get(self, product_id):
        """Get one Product"""

        product = Products()
        sql = product.get_one_product()
        cursor.execute(sql,(product_id,))
        data = cursor.fetchone()
        
        if data is None:
            return {'message' : 'Product not Found'},404

        return {
            'message' : 'success',
            'Product' : data
        },200

    @jwt_required
    def put(self, product_id):
        """Modify one Product: only by the admin """

        role = Users().get_user_role()

        if role[0] != "admin":
            return {
                "message" : "Access not allowed"
            },403

        data = parser.parse_args()
        name = data['name']
        price = data['price']
        quantity = data['quantity']
        min_quantity = data['min_quantity']
        category = data['category']

        if name.isalpha() == False:
            return {'message' : 'Invalid product name'},400

        if price.isdigit() == False:
            return {'message' : 'Invalid product price'},400
        
        if quantity.isdigit() == False:
            return {'message' : 'Invalid product quantity'},400

        if min_quantity.isdigit() == False:
            return {'message' : 'Invalid product minimum quantity'},400

        if category.isalpha() == False:
            return {'message' : 'Invalid product category'},400

        try:
            product = Products()
            sql = product.modify_product()
            cursor.execute(sql,(name,price,quantity,min_quantity,category,product_id))
            connection.commit()

            return {
                    'message': 'successfuly modified'
                },200
        except:
            return {'message': 'Product already exist'},409

    @jwt_required
    def delete(self, product_id):
        """delete one Product: only by the admin"""

        role = Users().get_user_role()

        if role[0] != "admin":
            return {
                "message" : "Access not allowed"
            },403

        try:
            product = Products()
            sql = product.delete_product()
            cursor.execute(sql,(product_id,))
            connection.commit()

            return {
                    'message': 'successfuly deleted'
                },200
        except:
            return {'message' : 'Product not found'},404

        
