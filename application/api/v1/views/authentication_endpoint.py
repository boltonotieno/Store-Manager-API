from flask_restful import Resource, reqparse
from ..models.user_model import Users
from passlib.hash import sha256_crypt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, 
jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from flask import jsonify


#passing incoming data into post requests
parser = reqparse.RequestParser()
parser.add_argument('name', help = 'This field cannot be blank', required = True)
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('email', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)
parser.add_argument('gender', help = 'This field cannot be blank', required = True)
parser.add_argument('role', help = 'This field cannot be blank', required = True)

parser_2 = reqparse.RequestParser()
parser_2.add_argument('username', help = 'This field cannot be blank', required = True)
parser_2.add_argument('password', help = 'This field cannot be blank', required = True)
class UserRegistration(Resource):
    def post(self):
        """Post new users"""
        data = parser.parse_args()
        name = data['name']
        username = data['username']
        email = data['email']
        password = sha256_crypt.encrypt((data['password']))
        gender = data['gender']
        role = data['role']

        new_user = Users()

        # if new_user.search_by_username(data['username']):
        #     return {
        #         'message' : 'User named {} already exist'.format( data['username'])
        #      }

        try:
            new_user.create_user(name,username,email,password,gender,role)
            return {
                'message': 'User named {} was created'.format( data['username']),
            },201

        except:
            return {'message' : 'something is wrong'}, 500

    def get(self):
        """Get all users"""
        all_users = Users.get_all_users(self)

        response = {
            'message' : 'success',
            'Users' : all_users},200
        
        return response

class GetUser(Resource):
    def get(self, user_id):
        """Get a single user"""
        user_obj= Users()

        response = jsonify(user_obj.get_one_user(user_id))
        response.status_code = 200

        return response

class UserLogin(Resource):
    def post(self):
        data = parser_2.parse_args()
        user_dict =[]
        user_dict.append(Users.get_user_dict(self))

        user = [user for user in user_dict if user[0]['username'] == data['username']]

        if not user:
            return {
                'message' : 'user {} does not exist'.format( data['username'])
            }

        if sha256_crypt.verify(data["password"], user[0][0]["password"]):
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message' : 'Logged in as {}'.format( user[0][0]['username']),
                'access token' : access_token,
                'refresh toke' : refresh_token
            }

        if data['password'] or data['username'] is None: 

            return {'message' : 'Enter all the fields'}

        if user[0][0]['username'] != data['username']:
            return {'message' : 'User jdoees does not exist'}
        else:
            return {
                'message' : 'wrong credentials'
            }


