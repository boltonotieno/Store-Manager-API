# /instance/config.py

import os

class Config(object):
    """Main  configuration class."""
    DEBUG = False

class DevelopmentConfig(Config):
    """Configurations for Development."""
    TESTING = True
    DEBUG = True

class TestingConfig(Config):
    """Configurations for Testing."""
    TESTING = True
    DEBUG = True

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
}
