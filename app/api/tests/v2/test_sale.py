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

    def tearDown(self):
        """Removes all initialised variables"""
        self.app_context.pop()

if __name__=='__main__':
    unittest.main()
    