import unittest
import os
import json
from app import create_app

class TestSales(unittest.TestCase):
    """Saless TestCases Class"""

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

        self.data_2 = {
            'name' : 'Tusker',
            'price' : '200'
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

    def test_post_sales(self):
        """Test if API can POST new sales"""

        #register user
        response_reg = self.client.post('/api/v2/auth/signup', 
        data= json.dumps(self.data_reg),
        content_type='application/json')

        #user login
        response_login = self.client.post('/api/v2/auth/login', 
        data= json.dumps(self.data_login),
        content_type='application/json')
        result_login = json.loads(response_login.data)
        token = result_login['access_token']

        #user post sales
        response = self.client.post('/api/v2/sales',
        headers = dict(Authorization='Bearer '+token),
        data= json.dumps(self.data),
        content_type='application/json')
        
        result = json.loads(response.data)
        self.assertEqual(result['message'], 'Created successfully' )
        self.assertEqual(response.status_code, 201)

    def test_post_sale_with_empty_fields(self):
        """Test if API can POST new sales with empty fields"""

        #register user
        response_reg = self.client.post('/api/v2/auth/signup', 
        data= json.dumps(self.data_reg),
        content_type='application/json')

        #user login
        response_login = self.client.post('/api/v2/auth/login', 
        data= json.dumps(self.data_login),
        content_type='application/json')
        result_login = json.loads(response_login.data)
        token = result_login['access_token']

        #user post sales
        response = self.client.post('/api/v2/sales',
        headers = dict(Authorization='Bearer '+token),
        data= json.dumps(self.data_2),
        content_type='application/json')
        
        result = json.loads(response.data)
        self.assertEqual(result['message'], {"quantity": "This field cannot be blank"})
        self.assertEqual(response.status_code, 400)


    def test_get_all_saless(self):
        """Test if API can GET all saless"""

        #register user
        response_reg = self.client.post('/api/v2/auth/signup', 
        data= json.dumps(self.data),
        content_type='application/json')

        #user login
        response_login = self.client.post('/api/v2/auth/login', 
        data= json.dumps(self.data_login),
        content_type='application/json')
        result_login = json.loads(response_login.data)
        token = result_login['access_token']

        #user post sales
        response_post = self.client.post('/api/v2/sales',
        headers = dict(Authorization='Bearer '+token),
        data= json.dumps(self.data),
        content_type='application/json')
        self.assertEqual(response_post.status_code, 201)

        
        #user get all saless
        response_get= self.client.get('/api/v2/sales',
        headers = dict(Authorization='Bearer '+token))
        result_get = json.loads(response_get.data)
        self.assertEqual(result_get['message'], 'success')
        self.assertEqual(response_get.status_code, 200)

    def test_get_sales_by_id(self):
        """Test if API can GET single sales by id"""

        #register user
        response_reg = self.client.post('/api/v2/auth/signup', 
        data= json.dumps(self.data),
        content_type='application/json')

        #user login
        response_login = self.client.post('/api/v2/auth/login', 
        data= json.dumps(self.data_login),
        content_type='application/json')
        result_login = json.loads(response_login.data)
        token = result_login['access_token']

        #user post sales
        response = self.client.post('/api/v2/sales', 
        headers = dict(Authorization='Bearer '+token),
        data= json.dumps(self.data),
        content_type='application/json')
        self.assertEqual(response.status_code, 201)

        #user get one sales
        response = self.client.get('/api/v2/sales/1',
        headers = dict(Authorization='Bearer '+token))
        result_get_one = json.loads(response.data)
        self.assertEqual(result_get_one['message'], 'success')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        """Removes all initialised variables"""
        self.app_context.pop()

if __name__=='__main__':
    unittest.main()
    