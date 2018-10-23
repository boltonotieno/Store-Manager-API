import unittest
import os
import json
from app import create_app

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
            'password' : 'jdoepass',
            'gender' : 'female',
            'role': 'admin'
        }
        
    def test_registration(self):
        """Test registration of new users"""
        response = self.client.post('/api/v2/auth/signup', 
        data= json.dumps(self.data),
        content_type='application/json')
        
        result = json.loads(response.data)
        self.assertEqual(result['message'], 'User created successfully' )
        self.assertEqual(response.status_code, 201)

    def test_empty_fields(self):
        """Test registration with missing username"""
        response = self.client.post('/api/v2/auth/signup', 
        data= json.dumps({
            'name' : 'Jane Doe',
            'email' : 'jdoe@gmail.com',
            'password' : 'jdoepass',
            'gender' : 'female',
            'role': 'admin'}),
        content_type='application/json')

        result = json.loads(response.data)
        self.assertEqual(result['message'], {"username": "This field cannot be blank"})
        self.assertEqual(response.status_code, 400)

    def test_invalid_email(self):
        """Test registration with invalid email"""
        response = self.client.post('/api/v2/auth/signup', 
        data= json.dumps({
            'name' : 'Jane Doe',
            'email' : 'jdoegmail.com',
            'password' : 'jdoepass',
            'gender' : 'female',
            'role': 'admin'}),
        content_type='application/json')

        result = json.loads(response.data)
        self.assertEqual(result['message'], {"Invalid Email"})
        self.assertEqual(response.status_code, 400)

    
    def test_get_all_users(self):
        """Test if API can GET all users"""
        response = self.client.post('/api/v2/auth/signup', 
        data= json.dumps(self.data),
        content_type='application/json')
        self.assertEqual(response.status_code, 201)
        
        response= self.client.get('/api/v2/users')
        result = json.loads(response.data)
        self.assertEqual(result['message'], 'success')
        self.assertEqual(response.status_code, 200)

    def test_get_user_by_id(self):
        """Test if API can GET single user by id"""
        response = self.client.post('/api/v2/auth/signup', 
        data= json.dumps(self.data),
        content_type='application/json')
        self.assertEqual(response.status_code, 201)

        response = self.client.get('/api/v2/users/1')
        result = json.loads(response.data)
        self.assertEqual(result['message'], 'success')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        """Removes all initialised variables"""
        self.app_context.pop()

