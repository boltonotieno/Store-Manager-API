import psycopg2
import os
from app import create_app


def db_connection():
    """Create Database Connection"""

    url = os.getenv('DATABASE_URL')          
    connection = psycopg2.connect(url)
    
    return connection

