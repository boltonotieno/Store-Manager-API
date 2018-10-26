from flask_restful import Resource, reqparse
import psycopg2
from flask import jsonify
from ..models.user_model import Users
from passlib.hash import sha256_crypt
from ..models import db_connection
from email_validator import validate_email

#passing incoming data into post requests
parser = reqparse.RequestParser()
parser.add_argument('name', help = 'This field cannot be blank', required = True)
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('email', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)
parser.add_argument('gender', help = 'This field cannot be blank', required = True)
parser.add_argument('role', help = 'This field cannot be blank', required = True)

class Registration(Resource):

    def post(self):
        """Post new users"""
        connection = db_connection()
        cursor = connection.cursor()

        data = parser.parse_args()
        name = data['name']
        username = data['username']
        email = data['email']
        password = sha256_crypt.encrypt((data['password']))
        gender = data['gender']
        role = data['role']

        #validate email
        try:
            validated_email = validate_email(email)
            valid_email = validated_email['email']
        except:
            return {'message' : 'Invalid Email'},400
        
        new_user = Users()
        sql = new_user.register_user()
        cursor.execute(sql,(name,username,valid_email,password,gender,role))
        connection.commit()
        
        return {
                'message': 'User created successfully',
            },201

    def get(self):
        """Get all Users"""

        connection = db_connection()
        cursor = connection.cursor()

        users = Users()
        sql = users.get_all_users()
        cursor.execute(sql)
        data = cursor.fetchall()

        if data is None:
            return {'message' : 'No users'}

        return {
                'message' : 'success',
                'Users' : data
            },200

class User(Resource):
    def get(self, user_id):
        """Get one User"""

        connection = db_connection()
        cursor = connection.cursor()

        users = Users()
        sql = users.get_one_user()
        cursor.execute(sql,(user_id,))
        data = cursor.fetchone()

        if data is None:
            return {'message' : 'User not Found'}

        return {
            'message' : 'success',
            'User' : data
        },200


        
