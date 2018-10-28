from flask_restful import Resource, reqparse
import psycopg2
from flask import jsonify
from ..models.category_model import Categories
from ..models.user_model import Users
from ..models import db_connection
from flask_jwt_extended import (create_access_token, jwt_required, get_jwt_claims, get_jwt_identity)

#passing incoming data into post requests
parser = reqparse.RequestParser()
parser.add_argument('name', help = 'This field cannot be blank', required = True)

connection = db_connection()
cursor = connection.cursor()

class Category(Resource):
    @jwt_required
    def post(self):
        """Post new category: only by the admin"""
        role = Users().get_user_role()

        data = parser.parse_args()
        name = data['name']

        if role[0] != "admin":
            return {
                "message" : "Access not allowed"
            },403
        
        if name.isalpha() == False:
            return{
                'message' : 'Invalid category name'
            },400
        else:
            try:
                new_category = Categories()
                sql = new_category.create_category()
                cursor.execute(sql,(name,))
                connection.commit()
                
                return {
                        'message': 'Category created successfully'
                    },201
            except:
                return {'message' : 'Category already exist'},409
    @jwt_required
    def get(self):
        """Get all Categories"""

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
    @jwt_required
    def get(self, category_id):
        """Get one Category"""

        category = Categories()
        sql = category.get_one_category()
        cursor.execute(sql,(category_id,))
        data = cursor.fetchone()

        if data is None:
            return {'message' : 'Category not Found'},404

        return {
            'message' : 'success',
            'Category' : data
        },200

    @jwt_required
    def put(self, category_id):
        """Modify one Category: only by the admin"""

        role = Users().get_user_role()

        if role[0] != "admin":
            return {
                "message" : "Access not allowed"
            },403

        data = parser.parse_args()
        name = data['name']

        try:
            category = Categories()
            sql = category.modify_category()
            cursor.execute(sql,(name,category_id))
            connection.commit()

            return {
                    'message': 'successfuly modified'
                },200
                
        except:
            return {'message': 'Category already exist'},409

    @jwt_required
    def delete(self, category_id):
        """delete one category: only by the admin"""

        role = Users().get_user_role()

        if role[0] != "admin":
            return {
                "message" : "Access not allowed"
            },403        
        try:
            category = Categories()
            sql = category.delete_category()
            cursor.execute(sql,(category_id,))
            connection.commit()

            return {
                  'message': 'successfuly deleted'
              },200

        except:
            return {'message' : 'Category not found'},404

