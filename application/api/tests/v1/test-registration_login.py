import unittest
import os
import json
from application.app import create_app

class TestAuthentication(unittest.TestCase):
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
            'password' : 'password',
            'gender' : 'female',
            'role': 'admin'
        }
        self.data_2 = {
            'name' : 'Jane Doe',
            'username' : 'jdoe',
            'email' : 'jdoe@gmail.com',
            'password' : 'password',
            'gender' : 'female',
            'role': 'admin'
        }

    def test_registration(self):
        """Test registeration of new users"""
        response = self.client.post('/api/v1/auth/registration', 
        data= json.dumps(self.data),
        content_type='application/json')
        
        result = json.loads(response.data)
        self.assertEqual(result['message'], 'User jdoe was created' )
        self.assertEqual(response.status_code, 201)

    def test_registration_of_existing_users(self):
        """Test registeration of existing users"""
        response = self.client.post('/api/v1/auth/registration', 
        data= json.dumps(self.data_2),
        content_type='application/json')
        
        result = json.loads(response.data)
        self.assertEqual(result['message'], 'User jdoe already exist')

    def test_empty_fields(self):
        """Test registeration of with an empty field"""
        response = self.client.post('/api/v1/auth/registration', 
        data= json.dumps({
            'name' : 'Jane Doe',
            'email' : 'jdoe@gmail.com',
            'password' : 'password',
            'gender' : 'female',
            'role': 'admin'}),
        content_type='application/json')

        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], {"username": "This field cannot be blank"})

    
