import unittest
import os
import json
from application.app import create_app

class TestProducts(unittest.TestCase):
    """Product TestCases Class"""

    def setUp(self):
        """ Define test variables"""
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.data = {
            'id' : 1,
            'name' : 'Pilsner',
            'price' : '200',
            'quantity' : '20',
            'category' : 'beer'
        }

    def tearDown(self):
        """Removes all initialised variables"""
        self.app_context.pop()