import unittest
import os
import json
from app import create_app

class TestLogin(unittest.TestCase):
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
            'username' : 'jdoe',
            'password' : 'jdoepass'
        }

    def tearDown(self):
        """Removes all initialised variables"""
        self.app_context.pop()

        