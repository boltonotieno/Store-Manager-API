import unittest
import os
import json
from application.app import create_app

class TestProducts(unittest.TestCase):
    """Sales TestCases Class"""

    def setUp(self):
        """ Define tests variables"""
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.data = {
            'name' : 'Tusker',
            'price' : '200',
            'quantity' : '5'
        }

        self.data_reg = {
            'name' : 'Jane Doe',
            'username' : 'jdoe',
            'email' : 'jdoe@gmail.com',
            'password' : 'jdoepass',
            'gender' : 'female',
            'role': 'admin'
        }
        self.data_login = {
            'username' : 'jdoe',
            'password' : 'jdoepass'
        }

    def test_post_sale(self):
        """Test if API can POST new sale"""

        #register user
        response_reg = self.client.post('/api/v1/auth/registration', 
        data= json.dumps(self.data_reg),
        content_type='application/json')

        #user login
        response_login = self.client.post('/api/v1/auth/login', 
        data= json.dumps(self.data_login),
        content_type='application/json')
        result_login = json.loads(response_login.data)
        token = result_login['access_token']

        #user post sale
        response = self.client.post('/api/v1/sale',
        headers = dict(Authorization='Bearer '+token),
        data= json.dumps(self.data),
        content_type='application/json')
        
        result = json.loads(response.data)
        self.assertEqual(result['message'], 'Created successfully' )
        self.assertEqual(response.status_code, 201)

    def test_get_all_sales(self):
        """Test if API can GET all sales"""

        #register user
        response_reg = self.client.post('/api/v1/auth/registration', 
        data= json.dumps(self.data),
        content_type='application/json')

        #user login
        response_login = self.client.post('/api/v1/auth/login', 
        data= json.dumps(self.data_login),
        content_type='application/json')
        result_login = json.loads(response_login.data)
        token = result_login['access_token']

        #user post sale
        response = self.client.post('/api/v1/sale',
        headers = dict(Authorization='Bearer '+token),
        data= json.dumps(self.data),
        content_type='application/json')
        self.assertEqual(response.status_code, 201)
        
        response= self.client.get('/api/v1/sale')
        result = json.loads(response.data)
        self.assertEqual(result['message'], 'success')
        self.assertEqual(response.status_code, 200)

    def test_get_sale_by_id(self):
        """Test if API can GET single sale by id"""

        #register user
        response_reg = self.client.post('/api/v1/auth/registration', 
        data= json.dumps(self.data),
        content_type='application/json')

        #user login
        response_login = self.client.post('/api/v1/auth/login', 
        data= json.dumps(self.data_login),
        content_type='application/json')
        result_login = json.loads(response_login.data)
        token = result_login['access_token']

        #user post sale
        response = self.client.post('/api/v1/sale', 
        headers = dict(Authorization='Bearer '+token),
        data= json.dumps(self.data),
        content_type='application/json')
        self.assertEqual(response.status_code, 201)

        response = self.client.get('/api/v1/sale/1')
        result = json.loads(response.data)
        self.assertEqual(result['message'], 'success')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        """Removes all initialised variables"""
        self.app_context.pop()

if __name__=='__main__':
    unittest.main()