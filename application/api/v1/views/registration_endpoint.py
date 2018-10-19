from flask_restful import Resource, reqparse
from ..models.user_model import Users
from passlib.hash import sha256_crypt
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, 
jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)


#passing incoming data into post requests
parser = reqparse.RequestParser()
parser.add_argument('name', help = 'This field cannot be blank', required = True)
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('email', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)
parser.add_argument('gender', help = 'This field cannot be blank', required = True)
parser.add_argument('role', help = 'This field cannot be blank', required = True)
class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()
        name = data['name']
        username = data['username']
        email = data['email']
        password = data['password']
        gender = data['gender']
        role = ['role']

        new_user = Users(name,username,email,password,gender,role)

        if new_user.search_by_username(data['username']):
            return {
                'message' : 'User named {} already exist'.format( data['username'])
            }

        try:
            new_user.create_user()
            return {
                'message': 'User named {} was created'.format( data['username']),
            },201

        except:
            return {'message' : 'something is wrong'}, 500
