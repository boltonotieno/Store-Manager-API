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


    def get(self):
        """Get all Categories"""

        connection = db_connection()
        cursor = connection.cursor()

        categories = Categories()
        sql = categories.get_all_category()
        cursor.execute(sql)
        data = cursor.fetchall()

        if len(data) == 0:
            return {'message' : 'No categories'}

        return {
                'message' : 'success',
                'Categories' : data
            },200

class SingleCategory(Resource):
    def get(self, category_id):
        """Get one Category"""

        connection = db_connection()
        cursor = connection.cursor()

        category = Categories()
        sql = category.get_one_category()
        cursor.execute(sql,(category_id,))
        data = cursor.fetchone()

        if data is None:
            return {'message' : 'Category not Found'}

        return {
            'message' : 'success',
            'Category' : data
        },200


    def put(self, category_id):
        """Modify one Category"""

        connection = db_connection()
        cursor = connection.cursor()

        data = parser.parse_args()
        name = data['name']

        category = Categories()
        sql = category.modify_category()
        cursor.execute(sql,(name,category_id))
        connection.commit()

        return {
                'message': 'successfuly modified'
            },200

