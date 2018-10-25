from flask_restful import Resource, reqparse
import psycopg2
from flask import jsonify
from ..models.category_model import Categories
from ..models import db_connection

#passing incoming data into post requests
parser = reqparse.RequestParser()
parser.add_argument('name', help = 'This field cannot be blank', required = True)

class Category(Resource):
    pass