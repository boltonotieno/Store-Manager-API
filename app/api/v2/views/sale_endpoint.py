from flask_restful import Resource, reqparse
import psycopg2
from flask import jsonify
from ..models.sale_model import Sales
from ..models.user_model import Users
from ..models import db_connection
from flask_jwt_extended import (create_access_token, jwt_required, get_jwt_claims, get_jwt_identity)
from ..utils import Validation

#passing incoming data into post requests
parser = reqparse.RequestParser()
parser.add_argument('name', help = 'This field cannot be blank', required = True)
parser.add_argument('price', help = 'This field cannot be blank', required = True)
parser.add_argument('quantity', help = 'This field cannot be blank', required = True)

connection = db_connection()

class Sale(Resource):

    
    @jwt_required
    def post(self):
        """Post new sales: only by the attendant"""

        cursor = connection.cursor()
        role = Users().get_user_role()

        if role[0] != "attendant":
            return {
                "message" : "Access allowed only to attendants"
            },403

        data = parser.parse_args()
        name = data['name']
        price = data['price']
        quantity = data['quantity']
        attendant = get_jwt_identity()

        if Validation(data).validate_sales:
            return Validation(data).validate_sales

        new_sales = Sales()
        sql = new_sales.create_sales()
        cursor.execute(sql,(name,price,quantity,attendant))
        connection.commit()
            
        return {
               'message': 'Sales created successfully',
                'attendant' : attendant
            },201
        # except:
        #     return {'message' : 'Sales Not Created'}

    @jwt_required
    def get(self):
        """Get all sales"""
        cursor = connection.cursor()

        role = Users().get_user_role()

        if role[0] != "admin":
            attendant_sales = Sales().get_attendant_all_sales()
            if len(attendant_sales) == 0:
                return {'message' : 'You have no sales'}

            return {
                "message" : "success",
                'Sales' : attendant_sales
            },200

        sales = Sales()
        sql = sales.get_all_sales()
        cursor.execute(sql)
        data = cursor.fetchall()

        if len(data) == 0:
            return {'message' : 'No sales'}

        return {
                'message' : 'success',
                'Sales' : data
            },200


class SingleSale(Resource):

    @jwt_required
    def get(self, sale_id):
        """Get one sale: only by the admin and creator of the sale"""

        
        cursor = connection.cursor()

        #get creator of sale
        sale = Sales()
        sql = sale.get_attendant_from_sales()
        cursor.execute(sql,(sale_id,))
        creator = cursor.fetchone()

        role = Users().get_user_role()
        current_user = get_jwt_identity()

        if creator is None:
            return {'message' : 'Sale id {} not found'.format(sale_id)},404

        if role[0] != "admin" and current_user != creator[0]:
            return {
                "message" : "Access not allowed"
            },403

        sale = Sales()
        sql = sale.get_one_sale()
        cursor.execute(sql,(sale_id,))
        data = cursor.fetchone()

        if data is None:
            return {'message' : 'Sale not Found'
            },404

        return {
            'message' : 'success',
            'Sale' : data
        },200

    @jwt_required
    def put(self, sale_id):
        """Modify one Sale: only by the admin"""

        
        cursor = connection.cursor()

        role = Users().get_user_role()

        if role[0] != "admin":
            return {
                "message" : "Access not allowed"
            },403

        data = parser.parse_args()
        name = data['name']
        price = data['price']
        quantity = data['quantity']

        if Validation(data).validate_sales():
            return Validation(data).validate_sales()

        try:
            sale = Sales()
            sql = sale.modify_sales()
            cursor.execute(sql,(name,price,quantity,sale_id))
            connection.commit()

            return {
                    'message': 'successfuly modified'
                },200
                
        except:
            return {'message': 'Sale not found'},404

    @jwt_required
    def delete(self, sale_id):
        """delete one sale : only by the admin"""

        cursor = connection.cursor()

        role = Users().get_user_role()

        if role[0] != "admin":
            return {
                "message" : "Access not allowed"
            },403

        try:
            sale = Sales()
            sql = sale.delete_sales()
            cursor.execute(sql,(sale_id,))
            connection.commit()

            return {
                  'message': 'successfuly deleted'
              },200

        except:
            return {'message' : 'Sale not found'},404

