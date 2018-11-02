from flask_restful import Resource, reqparse
import psycopg2
from flask import jsonify
from ..models.user_model import Users
from passlib.hash import sha256_crypt
from ..models import db_connection
from email_validator import validate_email
from ..utils import Validation
from flask_jwt_extended import (create_access_token, jwt_required,
                                get_jwt_identity)

# passing incoming data into post requests
parser = reqparse.RequestParser()
parser.add_argument('name', help='This field cannot be blank', required=True)
parser.add_argument('username', help='This field cannot be blank',
                    required=True)
parser.add_argument('email', help='This field cannot be blank', required=True)
parser.add_argument('password', help='This field cannot be blank',
                    required=True)
parser.add_argument('gender', help='This field cannot be blank', required=True)
parser.add_argument('role', help='This field cannot be blank', required=True)

# passing incoming data into put requests
parser_put = reqparse.RequestParser()
parser_put.add_argument('role', help='This field cannot be blank',
                        required=True)


class Registration(Resource):
    @jwt_required
    def post(self):
        """Post new users"""
        connection = db_connection()
        cursor = connection.cursor()

        role = Users().get_user_role()
        if role[0] != "admin":
            return {
                "message": "Access allowed only to admin"
            }, 403

        data = parser.parse_args()
        name = data['name']
        username = data['username']
        email = data['email']
        password = data['password']
        gender = data['gender'].lower()
        role = data['role'].lower()

        if Validation(data).validate_users():
            return Validation(data).validate_users()

        # validate email
        try:
            validated_email = validate_email(email)
            valid_email = validated_email['email']
        except:
            return {'message': 'Invalid Email'}, 400
        
        try:
            new_user = Users()
            sql = new_user.register_user()
            cursor.execute(sql, (name, username, valid_email,
                                 password, gender, role))
            connection.commit()

            users = Users()
            sql = users.get_one_user_username()
            cursor.execute(sql, (username,))
            data = cursor.fetchone()
            data_dict = {
                        'id': data[0],
                        'name': data[1],
                        'username': data[2],
                        'email': data[3],
                        'pasword': data[4],
                        'gender': data[5],
                        'role': data[6]
                }    
            
            return {
                    'message': 'User created successfully',
                    'User': data_dict
                }, 201

        except Exception as error:
            print(error)
            return {'message': 'User exist with the same username/email'}, 403

    @jwt_required
    def get(self):
        """Get all Users"""

        connection = db_connection()
        cursor = connection.cursor()

        role = Users().get_user_role()

        if role[0] != "admin":
            return {
                "message": "Access allowed only to admin"
            }, 403

        users = Users()
        sql = users.get_all_users()
        cursor.execute(sql)
        data = cursor.fetchall()

        if len(data) == 0:
            return {'message': 'No users'}

        data_list = []
        for datum in data:
            data_dict = {
                    'id': datum[0],
                    'name': datum[1],
                    'username': datum[2],
                    'email': datum[3],
                    'password': datum[4],
                    'gender': datum[5],
                    'role': datum[6]
                }   
            data_list.append(data_dict) 

        return {
                'message': 'Users successfully retrieved',
                'Users': data_list
            }, 200


class User(Resource):
    @jwt_required
    def get(self, user_id):
        """Get one User"""

        if user_id.isdigit() is False:
            return {'message': 'User id {} is invalid'.format(user_id)}

        connection = db_connection()
        cursor = connection.cursor()

        role = Users().get_user_role()

        if role[0] != "admin":
            return {
                "message": "Access allowed only to admin"
            }, 403
            
        users = Users()
        sql = users.get_one_user()
        cursor.execute(sql, (user_id,))
        data = cursor.fetchone()

        if data is None:
            return {'message': 'User not Found'}

        data_dict = {
                    'id': data[0],
                    'name': data[1],
                    'username': data[2],
                    'email': data[3],
                    'pasword': data[4],
                    'gender': data[5],
                    'role': data[6]
                    }
        return {
            'message': 'User successfully retrieved',
            'User': data_dict
        }, 200

    @jwt_required
    def put(self, user_id):
        """Change user role: only by the admin"""
        connection = db_connection()
        cursor = connection.cursor()

        current_role = Users().get_user_role()

        if current_role[0] != "admin":
            return {
                "message": "Access allowed only to admin"
            }, 403

        if user_id.isdigit() is False:
            return {'message': 'User id {} is invalid'.format(user_id)}, 400

        users = Users()
        sql = users.get_one_user()
        cursor.execute(sql, (user_id,))
        user_data = cursor.fetchone()

        if user_data is None:
            return {'message': 'User id {} not Found'.format(user_id)}

        if user_data[2] == 'admin':
            return {'message': 'Default admin cant be modified'}, 403

        data = parser_put.parse_args()
        role = data['role'].lower()

        if Validation(data).validate_role():
            return Validation(data).validate_role()

        if user_data[6] == 'admin' and role == 'admin':
            return{
                'message': 'User {} is already an admin'.format(user_data[2])
            }, 400

        if user_data[6] == 'attendant' and role == 'attendant':
            return{
                'message': 'User {} is already an attendant'
                .format(user_data[2])
            }, 400
    
        Users().modify_user_role(role, user_id)
        users = Users()
        sql = users.get_one_user()
        cursor.execute(sql, (user_id,))
        data = cursor.fetchone()
        data_dict = {
                    'id': data[0],
                    'name': data[1],
                    'username': data[2],
                    'email': data[3],
                    'pasword': data[4],
                    'gender': data[5],
                    'role': data[6]
                    }
        return {
                'message': 'User {} change role to {} succesfully'
                .format(data[1], role),
                'User': data_dict
                }, 200

    @jwt_required
    def delete(self, user_id):
        """delete one user: only by the admin"""

        if user_id.isdigit() is False:
            return {'message': 'User id {} is invalid'
                    .format(user_id)}, 400

        connection = db_connection()
        cursor = connection.cursor()

        role = Users().get_user_role()

        if role[0] != "admin":
            return {
                "message": "Access allowed only to admin"
            }, 403

        users = Users()
        sql = users.get_one_user()
        cursor.execute(sql, (user_id,))
        user_data = cursor.fetchone()

        if user_data is None:
            return {'message': 'User id {} not Found'.format(user_id)}

        if user_data[2] == 'admin':
            return {'message': 'Default admin cant be deleted'}, 403

        delete_user = Users()
        sql = delete_user.delete_user()
        cursor.execute(sql, (user_id,))
        connection.commit()

        return {
            'message': 'User id {} successfuly deleted'
            .format(user_id)
        }, 200

       