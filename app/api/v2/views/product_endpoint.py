from flask_restful import Resource, reqparse
import psycopg2
from flask import jsonify
from ..models.product_model import Products
from ..models.user_model import Users
from ..models.category_model import Categories
from ..models import db_connection
from flask_jwt_extended import (create_access_token, jwt_required, get_jwt_claims, get_jwt_identity)
from ..utils import Validation

#passing incoming data into post requests
parser = reqparse.RequestParser()
parser.add_argument('name', help = 'This field cannot be blank', required = True)
parser.add_argument('price', help = 'This field cannot be blank', required = True)
parser.add_argument('quantity', help = 'This field cannot be blank', required = True)
parser.add_argument('min_quantity', help = 'This field cannot be blank', required = True)
parser.add_argument('category_id', help = 'This field cannot be blank', required = True)

class Product(Resource):
    @jwt_required
    def post(self):
        """Post new products: only by the admin"""
        connection = db_connection()
        cursor = connection.cursor()

        role = Users().get_user_role()

        if role[0] != "admin":
            return {
                "message" : "Access allowed only to admin"
            },403

        data = parser.parse_args()
        name = data['name'].lower()
        price = data['price'].lower()
        quantity = data['quantity']
        min_quantity = data['min_quantity']
        category_id = data['category_id']

        if Validation(data).validate_product():
            return Validation(data).validate_product()

        #checks if category exists
        existing_category = Categories().get_one_category(category_id)
        if not existing_category:
            return {'message' : 'Category {} does not exist'.format(category_id)}

        try:
            new_product = Products()
            sql = new_product.create_product()
            cursor.execute(sql,(name,price,quantity,min_quantity,category_id))
            connection.commit()
            
            #fetch the added product
            data = Products().get_product__by_name(name)
            data_dict = {'id' : data[0],
                    'name' : data[1],
                    'price' : data[2],
                    'quantity' : data[3],
                    'min_quantity' : data[4],
                    'category_id' : data[5]
                }
            return {
                    'message': 'Product created successfully',
                    'Product': data_dict
                },201
        except Exception as e:
            print(e)
            return {'message' : 'Product {} already exist'.format(name)},409

    @jwt_required
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

        data_list = []
        for datum in data:  
            data_dict = {'id' : datum[0],
                        'name' : datum[1],
                        'price' : datum[2],
                        'quantity' : datum[3],
                        'min_quantity' : datum[4],
                        'category_id' : datum[5]
                        }
            data_list.append(data_dict)

        return {
                'message' : 'Products successfully retrieved',
                'Products' : data_list
            },200

class SingleProduct(Resource):
    @jwt_required
    def get(self, product_id):
        """Get one Product"""

        if product_id.isdigit() == False:
            return {'message' : 'Product id {} is invalid'.format(product_id)}

        data = Products().get_one_product(product_id)
        
        if data is None:
            return {'message' : 'Product not Found'},404

        data_dict = {'id' : data[0],
                    'name' : data[1],
                    'price' : data[2],
                    'quantity' : data[3],
                    'min_quantity' : data[4],
                    'category_id' : data[5]
                    }

        return {
            'message' : 'Product successfully retrieved',
            'Product' : data_dict
        },200

    @jwt_required
    def put(self, product_id):
        """Modify one Product: only by the admin """

        if product_id.isdigit() == False:
            return {'message' : 'Product id {} is invalid'.format(product_id)}

        connection = db_connection()
        cursor = connection.cursor()

        role = Users().get_user_role()

        if role[0] != "admin":
            return {
                "message" : "Access allowed only to admin"
            },403

        data = parser.parse_args()
        
        if Validation(data).validate_product():
            return Validation(data).validate_product()

        name = data['name'].lower()
        price = data['price']
        quantity = data['quantity']
        min_quantity = data['min_quantity']
        category_id = data['category_id']

        try:
            product = Products()
            sql = product.modify_product()
            cursor.execute(sql,(name,price,quantity,min_quantity,category_id,product_id))
            connection.commit()

            data = Products().get_one_product(product_id)
            if data is None:
                return {'message' : 'Product id {} not Found'.format(product_id)},404

            data_dict = {'id' : data[0],
                        'name' : data[1],
                        'price' : data[2],
                        'quantity' : data[3],
                        'min_quantity' : data[4],
                        'category_id' : data[5]
                        }      
            return {
                    'message' : 'Product id {} successfuly modified'.format(product_id),
                    'product' : data_dict
                },200
        except Exception as e:
            print(e)
            return {'message': 'Category id {} does not exist'.format(category_id)},404

    @jwt_required
    def delete(self, product_id):
        """delete one Product: only by the admin"""

        if product_id.isdigit() == False:
            return {'message' : 'Product id {} is invalid'.format(product_id)}

        connection = db_connection()
        cursor = connection.cursor()

        role = Users().get_user_role()

        if role[0] != "admin":
            return {
                "message" : "Access allowed only to admin"
            },403

        data = Products().get_one_product(product_id)
        if data is None:
            return {'message' : 'Product id {} not found'.format(product_id)},404

        product = Products()
        sql = product.delete_product()
        cursor.execute(sql,(product_id,))
        connection.commit()

        return {
                'message': 'Product id {} successfuly deleted'.format(product_id)
            },200

        
