import unittest
import os
import json
from app import create_app

class TestProducts(unittest.TestCase):
    """Product TestCases Class"""

    def setUp(self):
        """ Define test variables"""
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.data = {
            'name' : 'Pilsner',
            'price' : '200',
            'quantity' : '20',
            'min_quantity' : '5',
            'category' : 'beer'
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

    def test_post_product(self):
        """Test if API can POST new products"""

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

        #user post product
        response = self.client.post('/api/v2/products', 
        headers = dict(Authorization='Bearer '+token),
        data= json.dumps(self.data),
        content_type='application/json')
        
        result = json.loads(response.data)
        self.assertEqual(result['message'], 'Product created successfully' )
        self.assertEqual(response.status_code, 201)

    def test_get_all_products(self):
        """Test if API can GET all products"""

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

        #user post product
        response = self.client.post('/api/v2/products',
        headers = dict(Authorization='Bearer '+token),
        data= json.dumps(self.data),
        content_type='application/json')
        self.assertEqual(response.status_code, 201)
        
        #user get all product
        response= self.client.get('/api/v2/products',
        headers = dict(Authorization='Bearer '+token))
        result_get = json.loads(response.data)
        self.assertEqual(result_get['message'], 'success')
        self.assertEqual(response.status_code, 200)

    def test_get_product_by_id(self):
        """Test if API can GET single product by id"""

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

        #user post product
        response = self.client.post('/api/v2/products',
        headers = dict(Authorization='Bearer '+token),
        data= json.dumps(self.data),
        content_type='application/json')
        self.assertEqual(response.status_code, 201)

        #user get one product
        response = self.client.get('/api/v2/products/1',
        headers = dict(Authorization='Bearer '+token))
        result_get_one = json.loads(response.data)
        self.assertEqual(result_get_one['message'], 'success')
        self.assertEqual(response.status_code, 200)

    def test_modify_product(self):
        """Test if API can modify(PUT)  a single product"""
        
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

        #user post product
        response = self.client.post('/api/v2/products',
        headers = dict(Authorization='Bearer '+token),
        data= json.dumps(self.data),
        content_type='application/json')
        self.assertEqual(response.status_code, 201)

        #user modify product
        response_modify = self.client.put('/api/v2/products/1',
        headers = dict(Authorization='Bearer '+token),
        data= json.dumps({
            'name' : 'Pilsner',
            'price' : '300',
            'quantity' : '15',
            'min_quantity' : '5',
            'category' : 'beer'
            }),
        content_type='application/json')
        result_modify_one = json.loads(response_modify.data)
        self.assertEqual(result_modify_one['message'], 'successfuly modified')
        self.assertEqual(response_modify.status_code, 200)

    def test_delete_product(self):
        """Test if API can DELETE  a single product"""

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

        #user post product
        response = self.client.post('/api/v2/products',
        headers = dict(Authorization='Bearer '+token),
        data= json.dumps(self.data),
        content_type='application/json')
        self.assertEqual(response.status_code, 201)

        #user delete product
        response_delete = self.client.delete('/api/v2/products/1',
        headers = dict(Authorization='Bearer '+token))      
        result_delete_one = json.loads(response_delete.data)
        self.assertEqual(result_delete_one['message'], 'successfuly deleted')
        self.assertEqual(response_delete.status_code, 200)

        #Test if the product has been actually deleted by trying to GET it
        # response_get = self.client.get('/api/v2/products/1',
        # headers = dict(Authorization='Bearer '+token))
        # result_get = json.loads(response_get.data)
        # self.assertEqual(result_get['message'], 'Product not found')
        # self.assertEqual(response.status_code, 404)


    def tearDown(self):
        """Removes all initialised variables"""
        self.app_context.pop()

if __name__=='__main__':
    unittest.main()
