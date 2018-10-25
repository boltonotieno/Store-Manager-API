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
                    'message': 'Sales created successfully',
                },201
        except:
            return {'message' : 'Sales Not Created'}

