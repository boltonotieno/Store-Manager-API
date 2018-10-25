from flask_restful import Resource, reqparse
import psycopg2
from flask import jsonify
from ..models.category_model import Categories
from ..models import db_connection

#passing incoming data into post requests
parser = reqparse.RequestParser()
parser.add_argument('name', help = 'This field cannot be blank', required = True)

class Category(Resource):

    def post(self):
        """Post new category"""
        connection = db_connection()
        cursor = connection.cursor()

        data = parser.parse_args()
        name = data['name']
        
        new_category = Categories()
        sql = new_category.create_category()
        cursor.execute(sql,(name))
        connection.commit()
        
        return {
                'message': 'Category created successfully',
            },201
