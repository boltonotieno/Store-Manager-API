from flask_restful import Resource, reqparse
import psycopg2
from flask import jsonify
from ..models.sale_model import Sales
from ..models import db_connection

#passing incoming data into post requests
parser = reqparse.RequestParser()
parser.add_argument('name', help = 'This field cannot be blank', required = True)
parser.add_argument('price', help = 'This field cannot be blank', required = True)
parser.add_argument('quantity', help = 'This field cannot be blank', required = True)

class Sale(Resource):
    
    def post(self):
        """Post new sales"""
        connection = db_connection()
        cursor = connection.cursor()

        data = parser.parse_args()
        name = data['name']
        price = data['price']
        quantity = data['quantity']
        
        try:
            new_sales = Sales()
            sql = new_sales.create_sales()
            cursor.execute(sql,(name,price,quantity))
            connection.commit()
            
            return {
                    'message': 'Sales created successfully'
                },201
        except:
            return {'message' : 'Sales Not Created'}


    def get(self):
        """Get all sales"""

        connection = db_connection()
        cursor = connection.cursor()

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
    def get(self, sale_id):
        """Get one sale"""

        connection = db_connection()
        cursor = connection.cursor()

        sale = Sales()
        sql = sale.get_one_sale()
        cursor.execute(sql,(sale_id,))
        data = cursor.fetchone()

        if data is None:
            return {'message' : 'Sale not Found'}

        return {
            'message' : 'success',
            'Sale' : data
        },200

    
    def put(self, sale_id):
        """Modify one Sale"""

        connection = db_connection()
        cursor = connection.cursor()

        data = parser.parse_args()
        name = data['name']
        price = data['price']
        quantity = data['quantity']

        try:
            sale = Sales()
            sql = sale.modify_sales()
            cursor.execute(sql,(name,price,quantity,sale_id))
            connection.commit()

            return {
                    'message': 'successfuly modified'
                },200
                
        except:
            return {'message': 'Sale not found'}

    def delete(self, sale_id):
        """delete one sale"""

        connection = db_connection()
        cursor = connection.cursor()

        try:
            sale = Sales()
            sql = sale.delete_sales()
            cursor.execute(sql,(sale_id,))
            connection.commit()

            return {
                  'message': 'successfuly deleted'
              },200

        except:
            return {'message' : 'Sale not found'}

