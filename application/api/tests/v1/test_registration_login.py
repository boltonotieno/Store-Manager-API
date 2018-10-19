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
            'password' : 'jdoepass',
            'gender' : 'female',
            'role': 'admin'
        }
        self.data_2 = {
            'name' : 'Jane Doe',
            'username' : 'jdoe',
            'email' : 'jdoe@gmail.com',
            'password' : 'jdoepass',
            'gender' : 'female',
            'role': 'admin'
        }
        self.data_3 = {
            'username' : 'jdoe',
            'password' : 'jdoepass'
        }
        

    def test_registration(self):
        """Test registeration of new users"""
        response = self.client.post('/api/v1/auth/registration', 
        data= json.dumps(self.data),
        content_type='application/json')
        
        result = json.loads(response.data)
        self.assertEqual(result['message'], 'User named jdoe was created' )
        self.assertEqual(response.status_code, 201)

    def test_registration_of_existing_users(self):
        """Test registration of existing users"""
        response = self.client.post('/api/v1/auth/registration', 
        data= json.dumps(self.data_2),
        content_type='application/json')
        
        result = json.loads(response.data)
        self.assertEqual(result['message'], 'User named jdoe already exist')

    def test_empty_fields(self):
        """Test registration with missing username"""
        response = self.client.post('/api/v1/auth/registration', 
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

    def test_get_all_users(self):
        """Test if API can GET all users"""
        response = self.client.post('/api/v1/users', 
        data= json.dumps(self.data),
        content_type='application/json')
        self.assertEqual(response.status_code, 201)
        
        response= self.client.get('/api/v1/users')
        result = json.loads(response.data)
        self.assertEqual(result['message'], 'success')
        self.assertEqual(response.status_code, 200)

    def test_get_user_by_id(self):
        """Test if API can GET single user by id"""
        response = self.client.post('/api/v1/users/<int:user_id>', 
        data= json.dumps(self.data),
        content_type='application/json')
        self.assertEqual(response.status_code, 201)

        response = self.client.get('/api/v1/users/1')
        result = json.loads(response.data)
        self.assertEqual(result['message'], 'success')
        self.assertEqual(response.status_code, 200)


    def test_login(self):
        """Test login of users"""
        response = self.client.post('/api/v1/auth/login', 
        data= json.dumps(self.data_2),
        content_type='application/json')

        result = json.loads(response.data)
        self.assertEquals(result['message'], 'Logged in as jdoe ')
        self.assertEqual(response.status_code, 200)

    def test_login_with_invalid_username(self):
        """Test login with invalid username"""
        response = self.client.post('/api/v1/auth/login', 
        data= json.dumps({
            'username' : 'jdoees',
            'email' : 'jdoepass'}),
        content_type='application/json')

        result = json.load(response.data)
        self.assertEqual(result['message'], 'User jdoees does not exist')

    def test_login_with_wrong_passoword(self):
        """Test login with wrong password"""
        response = self.client.post('/api/v1/auth/login', 
        data= json.dumps({
            'username' : 'jdoe',
            'email' : 'jdoepassword'}),
        content_type='application/json')

        result = json.load(response.data)
        self.assertEqual(result['message'], 'Wrong credentials')


    def test_login_with_missing_field(self):
        """Test login with missing password"""
        response = self.client.post('/api/v1/auth/login',
        data= json.dumps({'username' : 'jdoe'}),
        content_type='application/json')

        result = json.loads(response.data)
        self.assertEquals(result['message'], {"password": "This field cannot be blank"})



