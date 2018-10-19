from flask_restful import Resource, reqparse
from ..models.user_model import Users
from ..models import user_model

from passlib.hash import sha256_crypt
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

        new_user.create_user(name,username,email,password,gender,role)
        
        return {
                'message': 'User named {} was created'.format( data['username']),
            },201


    def get(self):
        """Get all users"""
        all_users = Users.get_all_users(self)

        response = {
            'message' : 'success',
            'Users' : all_users},200
        
        return response

class GetUser(Resource):
    def get(self, username):
        """Get a single user"""
        user_obj= Users()

        response = jsonify(user_obj.get_one_user(username))
        response.status_code = 200

        return response

class UserLogin(Resource):
    def post(self):
        data = parser_2.parse_args()
        username = data['username']
        password = data['password']
        users_dict = user_model.users_dict

        if username in users_dict and sha256_crypt.verify(password, users_dict[username]['password']):
            access_token = create_access_token(identity = data['username'])
            return jsonify({
                'message' : 'Logged in as {}'.format( username),
                'access_token' : access_token
                })

        return {'message' : 'User {} does not exist'.format( data['username'])}
        
            # access_token = create_access_token(identity = data['username'])
            # refresh_token = create_refresh_token(identity = data['username'])
