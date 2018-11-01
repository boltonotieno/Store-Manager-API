import unittest
import os
import json
from app import create_app
from app.api.v2.models.user_model import Users
from app.api.v2.models.product_model import Products
from app.api.v2.models.category_model import Categories
from app.api.v2.models import create_tables, create_default_admin, drop_tables


class TestProducts(unittest.TestCase):
    """Product TestCases Class"""
    drop_tables()
    def setUp(self):
        """ Define test variables"""
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db_users = Users()
        self.db_category= Categories()  
        self.db_product= Products()
        with self.app.app_context():
            # create all tables
            self.db_category.create_table_category()
            self.db_product.create_table_products()
            create_default_admin()


        self.data = {
            'name' : 'Pilsner',
            'price' : '200',
            'quantity' : '20',
            'min_quantity' : '5',
            'category_id' : '1'
        }

        self.data_3 = {
            'name' : 'Tusker',
            'price' : '200',
            'quantity' : '20',
            'min_quantity' : '5',
            'category_id' : '1'
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
            'username' : 'admin',
            'password' : 'adminpass'
        }

    def test_post_product(self):
        """Test if API can POST new products"""
        #admin login
        response_login = self.client.post('/api/v2/auth/login', 
        data= json.dumps(self.data_login),
        content_type='application/json')
        result_login = json.loads(response_login.data)
        print(result_login)
        token = result_login['access_token']

        #user post category
        response_post = self.client.post('/api/v2/category', 
        headers = dict(Authorization='Bearer '+token),
        data= json.dumps({'name' : 'spirit'}),
        content_type='application/json')
        self.assertEqual(response_post.status_code, 201)

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

        #admin login
        response_login = self.client.post('/api/v2/auth/login', 
        data= json.dumps(self.data_login),
        content_type='application/json')
        result_login = json.loads(response_login.data)
        token = result_login['access_token']

        #user post product
        response = self.client.post('/api/v2/products',
        headers = dict(Authorization='Bearer '+token),
        data= json.dumps({
            'name' : 'Guinness',
            'price' : '200',
            'quantity' : '20',
            'min_quantity' : '5',
            'category_id' : '1'
        }),
        content_type='application/json')
        result = json.loads(response.data)
        print(response)
        self.assertEqual(result['message'], 'Product created successfully' )
        self.assertEqual(response.status_code, 201)
        
        #user get all product
        response= self.client.get('/api/v2/products',
        headers = dict(Authorization='Bearer '+token))
        result_get = json.loads(response.data)
        self.assertEqual(result_get['message'], 'Products successfully retrieved')
        self.assertEqual(response.status_code, 200)
               

    def test_get_product_by_id(self):
        """Test if API can GET single product by id"""

        #admin login
        response_login = self.client.post('/api/v2/auth/login', 
        data= json.dumps(self.data_login),
        content_type='application/json')
        result_login = json.loads(response_login.data)
        print(result_login)
        token = result_login['access_token']

        #user get one product
        response = self.client.get('/api/v2/products/2',
        headers = dict(Authorization='Bearer '+token))
        result_get_one = json.loads(response.data)
        self.assertEqual(result_get_one['message'], 'Product successfully retrieved')
        self.assertEqual(response.status_code, 200)

    def test_modify_product(self):
        """Test if API can modify(PUT)  a single product"""
        
        #admin login
        response_login = self.client.post('/api/v2/auth/login', 
        data= json.dumps(self.data_login),
        content_type='application/json')
        result_login = json.loads(response_login.data)
        print(result_login)
        token = result_login['access_token']

        #user post product
        response = self.client.post('/api/v2/products',
        headers = dict(Authorization='Bearer '+token),
        data= json.dumps({
            'name' : 'Kibao',
            'price' : '200',
            'quantity' : '20',
            'min_quantity' : '5',
            'category_id' : '1'
        }),
        content_type='application/json')
        self.assertEqual(response.status_code, 201)

        #user modify product
        response_modify = self.client.put('/api/v2/products/2',
        headers = dict(Authorization='Bearer '+token),
        data= json.dumps({
            'name' : 'Kibao',
            'price' : '300',
            'quantity' : '15',
            'min_quantity' : '5',
            'category_id' : '1'
            }),
        content_type='application/json')
        result_modify_one = json.loads(response_modify.data)
        self.assertEqual(result_modify_one['message'], 'successfuly modified')
        self.assertEqual(response_modify.status_code, 200)

    def test_delete_product(self):
        """Test if API can DELETE  a single product"""

        #admin login
        response_login = self.client.post('/api/v2/auth/login', 
        data= json.dumps(self.data_login),
        content_type='application/json')
        result_login = json.loads(response_login.data)
        print(result_login)
        token = result_login['access_token']

        #user post category
        response = self.client.post('/api/v2/category', 
        headers = dict(Authorization='Bearer '+token),
        data= json.dumps({'name' : 'beer'}),
        content_type='application/json')
        self.assertEqual(response.status_code, 201)

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
        self.assertEqual(result_delete_one['message'], 'Product id 1 successfuly deleted')
        self.assertEqual(response_delete.status_code, 200)

    def tearDown(self):
        """Removes all initialised variables"""
        # with self.app.app_context():
                # db_product= Products()
                # db_category= Categories()
                # self.db_product.drop_table_products()
                # self.db_category.drop_table_category()
        
        self.app_context.pop()
        # drop_tables()
        # db_product= Products()
        # db_category= Categories()
        # db_category.drop_table_category()
        # db_product.drop_table_products()
        

