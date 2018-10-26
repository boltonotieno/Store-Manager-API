import unittest
import os
import json
from app import create_app

class TestLogin(unittest.TestCase):
    """Authentication TestCases Class"""

    def setUp(self):
        """ Define tests variables"""
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.data = {
            'name' : 'Jane Doe',
            'username' : 'jdoe',
            'email' : 'jdoe@gmail.com',
            'password' : 'jdoepass',
            'gender' : 'female',
            'role': 'admin'
        }

        self.data_2 = {
            'username' : 'jdoe',
            'password' : 'jdoepass'
        }

    def test_login(self):
        """Test login of users"""  

        response = self.client.post('/api/v2/auth/registration', 
        data= json.dumps(self.data),
        content_type='application/json')
        self.assertEqual(response.status_code, 201)

        response = self.client.post('/api/v2/auth/login', 
        data= json.dumps(self.data_2),
        content_type='application/json')

        result = json.loads(response.data)
        self.assertEqual(result['message'], 'Logged in succesful')
        self.assertEqual(response.status_code, 200)


    def test_login_with_missing_field(self):
        """Test login with missing password"""
        response = self.client.post('/api/v2/auth/login',
        data= json.dumps({'username' : 'jdoe'}),
        content_type='application/json')

        result = json.loads(response.data)
        self.assertEqual(result['message'], {"password": "This field cannot be blank"})

    def tearDown(self):
        """Removes all initialised variables"""
        self.app_context.pop()

    