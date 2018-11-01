from flask_restful import Resource, reqparse
import psycopg2
from flask import jsonify
from ..models.sale_model import Sales
from ..models.user_model import Users
from ..models.product_model import Products
from ..models import db_connection
from flask_jwt_extended import (create_access_token, jwt_required,
                                get_jwt_identity)
from ..utils import Validation

# passing incoming data into post requests
parser = reqparse.RequestParser()
parser.add_argument('name', help='This field cannot be blank', required=True)
parser.add_argument('quantity', help='This field cannot be blank', 
                    required=True)

connection = db_connection()


class Sale(Resource):

    @jwt_required
    def post(self):
        """Post new sales: only by the attendant"""

        cursor = connection.cursor()
        role = Users().get_user_role()

        if role[0] != "attendant":
            return {
                "message": "Access allowed only to attendants"
            }, 403

        data = parser.parse_args()
        name = data['name'].lower()
        quantity = data['quantity']
        attendant = get_jwt_identity()

        if Validation(data).validate_sales():
            return Validation(data).validate_sales()
        
        # checks if product exists
        existing_product = Products().get_product__by_name(name)
        if not existing_product:
            return {'message': 'Product does not exist'}, 404

        product_price = Products().get_product_price(name)
        product_quantity = Products().get_product_quantity(name)
        product_min_quantity = Products().get_product_min_quantity(name)
        new_quantity = int(product_quantity) - int(quantity)

        # check if min_quantity  has been reached
        if product_quantity <= product_min_quantity:
            return {'message': 'Product has reached the minimum quantity'}

        # check if new quanity will below the min_quanity
        if new_quantity < product_min_quantity:
            return {'message': 'Product quantity will go below \
            the minimum quantity allowed'}

        # check if inventory quantity is not enough
        if int(quantity) > product_quantity:
            return {'message': 'Product quantity is more than available \
            inventory quantity '}

        new_sales = Sales()
        sql = new_sales.create_sales()
        cursor.execute(sql, (name, product_price, quantity, attendant))
        connection.commit()

        Products().reduce_product_quantity(new_quantity, name)
        return {
                'message': 'Sales created successfully',
                'attendant': attendant
            }, 201

    @jwt_required
    def get(self):
        """Get all sales"""
        cursor = connection.cursor()

        role = Users().get_user_role()

        if role[0] != "admin":
            attendant_sales = Sales().get_attendant_all_sales()
            if len(attendant_sales) == 0:
                return {'message': 'You have no sales'}

            data_list = []
            for attendant_sale in attendant_sales:
                data_dict = {
                            'id': attendant_sale[0],
                            'name': attendant_sale[1],
                            'price': attendant_sale[2],
                            'quantity': attendant_sale[3],
                            'attendant': attendant_sale[4],
                            'total_price': attendant_sale[5]
                            }
                data_list.append(data_dict)

            return {
                "message": "Sales successfully retrieved",
                'Sales': data_list
            }, 200

        sales = Sales()
        sql = sales.get_all_sales()
        cursor.execute(sql)
        data = cursor.fetchall()

        if len(data) == 0:
            return {'message': 'No sales'}
        
        data_list = []
        for datum in data:
            data_dict = {
                        'id': datum[0],
                        'name': datum[1],
                        'price': datum[2],
                        'quantity': datum[3],
                        'attendant': datum[4],
                        'total_price': datum[5]
                        }
            data_list.append(data_dict)

        return {
                'message': 'Sales successfully retrieved',
                'Sales': data_list
            }, 200


class SingleSale(Resource):

    @jwt_required
    def get(self, sale_id):
        """Get one sale: only by the admin and creator of the sale"""

        if sale_id.isdigit() is False:
            return {'message': 'Sale id {} is invalid'.format(sale_id)}
        
        cursor = connection.cursor()

        # get creator of sale
        sale = Sales()
        sql = sale.get_attendant_from_sales()
        cursor.execute(sql, (sale_id,))
        creator = cursor.fetchone()

        role = Users().get_user_role()
        current_user = get_jwt_identity()

        if creator is None:
            return {'message': 'Sale id {} not found'.format(sale_id)}, 404

        if role[0] != "admin" and current_user != creator[0]:
            return {
                "message": "Access allowed only to admin and \
                creator of the sale"
            }, 403

        # fetch the sale
        data = Sales().get_one_sale(sale_id)

        if data is None:
            return {'message': 'Sale not Found'}, 404
        
        data_dict = {
                    'id': data[0],
                    'name': data[1],
                    'price': data[2],
                    'quantity': data[3],
                    'attendant': data[4],
                    'total_price': data[5]
                    }

        return {
            'message': 'Sale successfully retrieved',
            'Sale': data_dict
        }, 200

    @jwt_required
    def put(self, sale_id):
        """Modify one Sale: only by the admin"""

        if sale_id.isdigit() is False:
            return {'message': 'Sale id {} is invalid'.format(sale_id)}
        
        cursor = connection.cursor()

        role = Users().get_user_role()

        if role[0] != "admin":
            return {
                "message": "Access allowed only to admin"
            }, 403

        data = parser.parse_args()
        name = data['name']
        quantity = data['quantity']
    
        # search for the product
        product = Products().get_product__by_name(name)
        if product is None:
            return {'message': 'Product named {} not found'.format(name)}, 404

        # get product price
        product_price = Products().get_product_price(name)

        if Validation(data).validate_sales():
            return Validation(data).validate_sales()

        try:
            sale = Sales()
            sql = sale.modify_sales()
            cursor.execute(sql, (name, product_price, quantity, sale_id))
            connection.commit()

            # fetch the sale
            data = Sales().get_one_sale(sale_id)
            
            data_dict = {
                        'id': data[0],
                        'name': data[1],
                        'price': data[2],
                        'quantity': data[3],
                        'attendant': data[4],
                        'total_price': data[5]
                        }

            return {
                    'message': 'Sale id {} successfuly modified'
                    .format(sale_id),
                    'sale': data_dict
                }, 200
                
        except:
            return {'message': 'Sale id {} not found'.format(sale_id)}, 404

    @jwt_required
    def delete(self, sale_id):
        """delete one sale : only by the admin"""

        if sale_id.isdigit() is False:
            return {'message': 'Sale id {} is invalid'.format(sale_id)}

        cursor = connection.cursor()

        role = Users().get_user_role()

        if role[0] != "admin":
            return {
                "message": "Access allowed only to admin"
            }, 403

        try:
            sale = Sales()
            sql = sale.delete_sales()
            cursor.execute(sql, (sale_id,))
            connection.commit()

            return {
                  'message': 'successfuly deleted'
              }, 200

        except:
            return {'message': 'Sale not found'}, 404

