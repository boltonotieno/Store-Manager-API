from flask import Flask, Blueprint
from flask_restplus import Api

version1 = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(version1)

