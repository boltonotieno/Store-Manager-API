from flask_restful import Resource, reqparse
import psycopg2
from ..models.user_model import Users
from ..models import db_connection
from flask_jwt_extended import (create_access_token, jwt_required, get_jwt_claims, get_jwt_identity,
get_current_user, get_raw_jwt)
from passlib.hash import sha256_crypt
from flask import jsonify

TOKEN_BLACKLIST = set()

#passing incoming data into post requests
parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)

class Login(Resource):
    def post(self):
        """Logs in a User"""
        connection = db_connection()
        cursor = connection.cursor()

        data = parser.parse_args()
        username = data['username']
        password = data['password']

        user = Users()
        sql = user.get_user_by_username()
        cursor.execute(sql,(username,))
        data = cursor.fetchone()
    
    

        if not data:
            return {'message' : 'User named {} not found'.format( username)}
        
        if password in data:
            access_token = create_access_token(identity=username)
            return {
                    'message' : 'Logged in succesful',
                    'access_token' : access_token
             }
    

        return {'message' : 'Invalid password'}


class Logout(Resource):

    @jwt_required
    def delete(self):
        """ Logs out a user by revoking the access token """
        jti = get_raw_jwt()['jti']
        try:
            TOKEN_BLACKLIST.add(jti)
            return {"message": "Logged out succesful"}, 200
        except:
            return {'message': 'Something went wrong'}, 500

