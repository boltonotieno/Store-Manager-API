from flask_restful import Resource, reqparse
from ..models.user_model import Users
from ..models import user_model

from passlib.hash import sha256_crypt
from flask import jsonify

#passing incoming data into post requests
parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)

class Login(Resource):
    def post(self):
        pass
