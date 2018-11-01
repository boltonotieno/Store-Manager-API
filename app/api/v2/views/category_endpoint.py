import re
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

class Category(Resource):
    @jwt_required
    def post(self):
        """Post new category: only by the admin"""
        connection = db_connection()
        cursor = connection.cursor()

        role = Users().get_user_role()
        print(role)
        if role[0] != "admin":
            return {
                "message" : "Access allowed only to admin"
            },403

        data = parser.parse_args()
        name = data['name'].lower()        
        if name.isalpha() == False:
            return{
                'message' : 'Invalid category name {}'.format(name)
            },400
        
        try:
            new_category = Categories()
            sql = new_category.create_category()
            cursor.execute(sql,(name,))
            connection.commit()

            #fetch the added category
            data = Categories().get_category__by_name(name)
            data_dict = {'id' : data[0],
                        'name' : data[1],
                    }

            return {
                    'message' : 'Category created successfully',
                    'Category' : data_dict
                },201
        except:
            return {'message' : 'Category {} already exist'.format(name)},409

    @jwt_required
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

        data_list = []
        for datum in data:  
            data_dict = {'id' : datum[0],
                        'name' : datum[1],
                        }
            data_list.append(data_dict)

        return {
                'message' : 'Categories successfully retrieved',
                'Categories' : data_list
            },200

class SingleCategory(Resource):
    @jwt_required
    def get(self, category_id):
        """Get one Category"""
        if category_id.isdigit() == False:
            return {'message' : 'Category id {} is invalid'.format(category_id)},400

        data = Categories().get_one_category(category_id)

        if data is None:
            return {'message' : 'Category id {} not Found'.format(category_id)},404

        data_dict = {'id' : data[0],
                    'name' : data[1],
                    }        

        return {
            'message' : 'Category successfully retrieved',
            'Category' : data_dict
        },200

    @jwt_required
    def put(self, category_id):
        """Modify one Category: only by the admin"""
        connection = db_connection()
        cursor = connection.cursor()

        role = Users().get_user_role()

        if role[0] != "admin":
            return {
                "message" : "Access allowed only to admin"
            },403

        if category_id.isdigit() == False:
            return {'message' : 'Category id {} is invalid'.format(category_id)},400

        data = parser.parse_args()
        name = data['name'].lower()       
        if name.isalpha() == False:
            return{
                'message' : 'Invalid category name {}'.format(name)
            },400

        try:
            put_category = Categories()
            sql = put_category.modify_category()
            cursor.execute(sql,(name,category_id))
            connection.commit()

            data = Categories().get_one_category(category_id)
            if data is None:
                return {'message' : 'Category id {} not Found'.format(category_id)},404
                
            data_dict = {'id' : data[0],
                        'name' : data[1],
                    }        
            return {
                    'message': 'Category id {} successfuly modified'.format(category_id),
                    'Category' : data_dict
                },200
                
        except:
            return {'message': 'Category {} already exist'.format(name)},409

    @jwt_required
    def delete(self, category_id):
        """delete one category: only by the admin"""
        if category_id.isdigit() == False:
            return {'message' : 'Category id {} is invalid'.format(category_id)},400

        connection = db_connection()
        cursor = connection.cursor()

        role = Users().get_user_role()

        if role[0] != "admin":
            return {
                "message" : "Access allowed only to admin"
            },403        
        
        try:
            data = Categories().get_one_category(category_id)
            if data is None:
                return {'message' : 'Category id {} not Found'.format(category_id)},404

            del_category = Categories()
            sql = del_category.delete_category()
            cursor.execute(sql,(category_id,))
            connection.commit()

            return {
                'message': 'Category id {} successfuly deleted'.format(category_id)
            },200

        except Exception as e:
            print(e)
            return {'message' : 'There exist a product with category_id {}'.format(category_id)},400
        

