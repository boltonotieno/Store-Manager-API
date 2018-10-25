from flask_restful import Resource, reqparse
import psycopg2
from ..models.user_model import Users
from ..models import db_connection

from passlib.hash import sha256_crypt
from flask import jsonify

#passing incoming data into post requests
parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)

class Login(Resource):
    def post(self):

        connection = db_connection()
        cursor = connection.cursor()

        data = parser.parse_args()
        username = data['username']
        password = data['password']

        user = Users()
        sql = user.get_user_by_username()
        cursor.execute(sql,(username,))
        data = cursor.fetchone()

        if data is None:
            return {'message' : 'User named {} not found'.format( username)}
        
        
        # if sha256_crypt.verify(password, data[0][0]):

        #     return {'message' : 'Logged in succesful'}

        return {'message' : 'Logged in succesful'}
