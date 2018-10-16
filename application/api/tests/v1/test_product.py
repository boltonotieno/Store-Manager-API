import unittest
import os
import json
from application import create_app

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
            'category' : 'beer'
        }

    def test_post_product(self):
        """Test if API can post new products"""
        response = self.client.post('/product', data=self.data)

        self.assertEqual(response.status_code, 201)


    def tearDown(self):
        """Removes all initialised variables"""
        self.app_context.pop()

if __name__=='__main__':
    unittest.main()