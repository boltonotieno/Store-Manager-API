import unittest
from application.app import create_app

class BaseTestcase(unittest.TestCase):
    """This class represents the Base Test"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Removes all the initialised variables"""
        self.app_context.pop()

