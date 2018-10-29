import unittest
import os
import json
from app import create_app
from app.api.v2.models.user_model import Users
from app.api.v2.models.category_model import Categories

class TestCategory(unittest.TestCase):
    """category TestCases Class"""

    def setUp(self):
        """ Define test variables"""
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        with self.app.app_context():
            # create all tables
            db_user = Users()
            db_category = Categories()
            db_user.create_table_user()
            db_category.create_table_category()

        self.data = {
            'name' : 'beer'
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

    def test_post_category(self):
        """Test if API can POST new product category"""

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

        #user post category
        response = self.client.post('/api/v2/category', 
        headers = dict(Authorization='Bearer '+token),
        data= json.dumps(self.data),
        content_type='application/json')
        
        result = json.loads(response.data)
        self.assertEqual(result['message'], 'Category created successfully' )
        self.assertEqual(response.status_code, 201)

    def test_get_all_category(self):
        """Test if API can GET all category"""

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

        #user post category
        response = self.client.post('/api/v2/category',
        headers = dict(Authorization='Bearer '+token),
        data= json.dumps(self.data),
        content_type='application/json')
        self.assertEqual(response.status_code, 201)
        
        #user get all category
        response= self.client.get('/api/v2/category',
        headers = dict(Authorization='Bearer '+token))
        result_get = json.loads(response.data)
        self.assertEqual(result_get['message'], 'success')
        self.assertEqual(response.status_code, 200)

    def test_get_category_by_id(self):
        """Test if API can GET single category by id"""

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

        #user post category
        response = self.client.post('/api/v2/category',
        headers = dict(Authorization='Bearer '+token),
        data= json.dumps(self.data),
        content_type='application/json')
        self.assertEqual(response.status_code, 201)

        #user get one category
        response = self.client.get('/api/v2/category/1',
        headers = dict(Authorization='Bearer '+token))
        result_get_one = json.loads(response.data)
        self.assertEqual(result_get_one['message'], 'success')
        self.assertEqual(response.status_code, 200)

    def test_modify_category(self):
        """Test if API can modify(PUT) a single category"""
        
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

        #user post category
        response = self.client.post('/api/v2/category',
        headers = dict(Authorization='Bearer '+token),
        data= json.dumps(self.data),
        content_type='application/json')
        self.assertEqual(response.status_code, 201)

        #user modify category
        response_modify = self.client.put('/api/v2/category/1',
        headers = dict(Authorization='Bearer '+token),
        data= json.dumps({'name' : 'spirit'}),
        content_type='application/json')
        result_modify_one = json.loads(response_modify.data)
        self.assertEqual(result_modify_one['message'], 'successfuly modified')
        self.assertEqual(response_modify.status_code, 200)

    def test_delete_category(self):
        """Test if API can DELETE  a single category"""

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

        #user post category
        response = self.client.post('/api/v2/category',
        headers = dict(Authorization='Bearer '+token),
        data= json.dumps(self.data),
        content_type='application/json')
        self.assertEqual(response.status_code, 201)

        #user delete category
        response_delete = self.client.delete('/api/v2/category/1',
        headers = dict(Authorization='Bearer '+token))      
        result_delete_one = json.loads(response_delete.data)
        self.assertEqual(result_delete_one['message'], 'successfuly deleted')
        self.assertEqual(response_delete.status_code, 200)

        #Test if the category has been actually deleted by trying to GET it
        response_get = self.client.get('/api/v2/category/1',
        headers = dict(Authorization='Bearer '+token))
        result_get = json.loads(response_get.data)
        self.assertEqual(result_get['message'], 'Category not Found')


    def tearDown(self):
        """Removes all initialised variables"""
        self.app_context.pop()
        db_user = Users()
        db_category= Categories()
        db_user.drop_table_user()
        db_category.drop_table_category()

if __name__=='__main__':
    unittest.main()
