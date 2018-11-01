import unittest
import os
import json
from app import create_app
from app.api.v2.models.user_model import Users
from app.api.v2.models import create_tables, create_default_admin, drop_tables


class TestLogin(unittest.TestCase):
    """Authentication TestCases Class"""
    drop_tables()

    def setUp(self):
        """ Define tests variables"""
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        with self.app.app_context():
            #  create all tables
            db = Users()
            db.create_table_user()

        self.data = {
            'name': 'Jane Doe',
            'username': 'jdoe',
            'email': 'jdoe@gmail.com',
            'password': 'jdoepass',
            'gender': 'female',
            'role': 'admin'
        }

        self.data_2 = {
            'username': 'jdoe',
            'password': 'jdoepass'
        }

        self.data_login = {
            'username': 'admin',
            'password': 'adminpass'
        }

    def test_login(self):
        """Test login of users"""  

        # admin login
        response_login = self.client.post('/api/v2/auth/login', 
                                          data=json.dumps(self.data_login),
                                          content_type='application/json')
        result_login = json.loads(response_login.data)
        token = result_login['access_token']

        response = self.client.post('/api/v2/auth/signup',
                                    headers=dict(
                                        Authorization='Bearer '+token),
                                    data=json.dumps(self.data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)

        response = self.client.post(
                                '/api/v2/auth/login', 
                                data=json.dumps(self.data_2),
                                content_type='application/json')

        result = json.loads(response.data)
        self.assertEqual(result['message'], 'Logged in succesful as jdoe')
        self.assertEqual(response.status_code, 200)

    def test_login_with_missing_field(self):
        """Test login with missing password"""
        response = self.client.post(
                                '/api/v2/auth/login',
                                data=json.dumps({'username': 'jdoe'}),
                                content_type='application/json')

        result = json.loads(response.data)
        self.assertEqual(
            result['message'], {"password": "This field cannot be blank"})

    def tearDown(self):
        """Removes all initialised variables"""
        self.app_context.pop()

      