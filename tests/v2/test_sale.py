import unittest
import os
import json
from app import create_app
from app.api.v2.models.user_model import Users
from app.api.v2.models.sale_model import Sales
from app.api.v2.models.category_model import Categories
from app.api.v2.models.product_model import Products

class TestSales(unittest.TestCase):
    """Saless TestCases Class"""

    def setUp(self):
        """ Define tests variables"""
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        with self.app.app_context():
            # create all tables
            db_user = Users()
            db_sale = Sales()
            db_category = Categories()
            db_product = Products()

            db_user.create_table_user()
            db_category.create_table_category()
            db_product.create_table_products()
            db_sale.create_table_sales()

        self.data = {
            'name' : 'Tusker',
            'quantity' : '5'
        }

        self.data_2 = {
            'name' : 'Tusker',
        }

        self.data_reg = {
            'name' : 'Jane Doe',
            'username' : 'jdoe',
            'email' : 'jdoe@gmail.com',
            'password' : 'jdoepass',
            'gender' : 'female',
            'role': 'attendant'
        }

        self.data_prod = {
            'name' : 'Pilsner',
            'price' : '200',
            'quantity' : '20',
            'min_quantity' : '5',
            'category' : 'beer'
        }

        self.data_cat = {
            'name' : 'beer'
        }
    
        self.data_login = {
            'username' : 'jdoe',
            'password' : 'jdoepass'
        }

        self.data_admin = {
            'username' : 'admin',
            'password' : 'adminpass'
        }

    def test_post_sales(self):
        """Test if API can POST new sales"""

        #admin login
        response_login = self.client.post('/api/v2/auth/login', 
        data= json.dumps(self.data_admin),
        content_type='application/json')
        result_login = json.loads(response_login.data)
        token = result_login['access_token']

        #admin post category
        response = self.client.post('/api/v2/category',
        headers = dict(Authorization='Bearer '+token),
        data= json.dumps(self.data),
        content_type='application/json')
        self.assertEqual(response.status_code, 201)

        #admin post product
        response = self.client.post('/api/v2/products', 
        headers = dict(Authorization='Bearer '+token),
        data= json.dumps(self.data),
        content_type='application/json')

        #register user
        response_reg = self.client.post('/api/v2/auth/signup',
        headers = dict(Authorization='Bearer '+token),
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
        self.assertEqual(result['message'], 'Sales created successfully' )
        self.assertEqual(response.status_code, 201)

    # def test_post_sale_with_empty_fields(self):
    #     """Test if API can POST new sales with empty fields"""

    #     #admin login
    #     response_login = self.client.post('/api/v2/auth/login', 
    #     data= json.dumps(self.data_admin),
    #     content_type='application/json')
    #     result_login = json.loads(response_login.data)
    #     token = result_login['access_token']

    #     #register user
    #     response_reg = self.client.post('/api/v2/auth/signup',
    #     headers = dict(Authorization='Bearer '+token),
    #     data= json.dumps(self.data_reg),
    #     content_type='application/json')

    #     #user login
    #     response_login = self.client.post('/api/v2/auth/login', 
    #     data= json.dumps(self.data_login),
    #     content_type='application/json')
    #     result_login = json.loads(response_login.data)
    #     token = result_login['access_token']

    #     #user post sales
    #     response = self.client.post('/api/v2/sales',
    #     headers = dict(Authorization='Bearer '+token),
    #     data= json.dumps(self.data_2),
    #     content_type='application/json')
        
    #     result = json.loads(response.data)
    #     self.assertEqual(result['message'], {"quantity": "This field cannot be blank"})
    #     self.assertEqual(response.status_code, 400)

    # def test_modify_sales(self):
    #     """Test if API can modify(PUT) a single sale"""

    #     #register user
    #     response_reg = self.client.post('/api/v2/auth/signup', 
    #     data= json.dumps(self.data_reg),
    #     content_type='application/json')

    #     #attendant login
    #     response_login = self.client.post('/api/v2/auth/login', 
    #     data= json.dumps(self.data_login),
    #     content_type='application/json')
    #     result_login = json.loads(response_login.data)
    #     token = result_login['access_token']

    #     #attendant post sales
    #     response = self.client.post('/api/v2/sales',
    #     headers = dict(Authorization='Bearer '+token),
    #     data= json.dumps(self.data),
    #     content_type='application/json')
    #     self.assertEqual(response.status_code, 201)
        
    #     #register user
    #     response_reg = self.client.post('/api/v2/auth/signup', 
    #     data= json.dumps({
    #         'name' : 'John Doe',
    #         'username' : 'johnd',
    #         'email' : 'johnd@gmail.com',
    #         'password' : 'johndpass',
    #         'gender' : 'male',
    #         'role': 'admin'
    #     }),
    #     content_type='application/json')

    #     #admin login
    #     response_login = self.client.post('/api/v2/auth/login', 
    #     data= json.dumps({
    #         'username' : 'johnd',
    #         'password' : 'johndpass'
    #     }),
    #     content_type='application/json')
    #     result_login = json.loads(response_login.data)
    #     token = result_login['access_token']

    #     #user modify sales
    #     response_modify = self.client.put('/api/v2/sales/1',
    #     headers = dict(Authorization='Bearer '+token),
    #     data= json.dumps({
    #         'name' : 'Tusker',
    #         'price' : '200',
    #         'quantity' : '10'
    #         }),
    #     content_type='application/json')
    #     result_modify_one = json.loads(response_modify.data)
    #     self.assertEqual(result_modify_one['message'], 'successfuly modified')
    #     self.assertEqual(response_modify.status_code, 200)


    def tearDown(self):
        """Removes all initialised variables"""
        self.app_context.pop()
        db_user = Users()
        db_sale = Sales()
        db_category = Categories()
        db_product = Products()
        db_user.drop_table_user()
        db_category.drop_table_category()
        db_product.drop_table_products()
        db_sale.drop_table_sales()


if __name__=='__main__':
    unittest.main()
    