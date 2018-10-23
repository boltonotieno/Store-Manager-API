# /instance/config.py

import os

class Config(object):
    """Main  configuration class."""
    DEBUG = False
    DATABASE_URL = os.getenv('DATABASE_URL')

class DevelopmentConfig(Config):
    """Configurations for Development."""
    TESTING = True
    DEBUG = True

class TestingConfig(Config):
    """Configurations for Testing."""
    TESTING = True
    DEBUG = True
    DATABASE_URL="dbname='test_store_manager' host='localhost' port='5432' user='bolt' password='root123!'"

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
}
