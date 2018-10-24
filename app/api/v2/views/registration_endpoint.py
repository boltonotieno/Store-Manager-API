from flask_restful import Resource, reqparse
import psycopg2
from flask import jsonify
from ..models.user_model import Users
from passlib.hash import sha256_crypt
from ..models import db_connection

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

        new_user = Users()
        sql = new_user.register_user()
        cursor.execute(sql,(name,username,email,password,gender,role))
        
        return {
                'message': 'User created successfully',
            },201



