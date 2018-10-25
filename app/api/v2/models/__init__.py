import psycopg2
import os
from .database_model import Database

def db_connection():
    """Create Database Connection"""

    url = os.getenv('DATABASE_URL')          
    connection = psycopg2.connect(url)
    
    return connection

def create_tables():
    """Creates the Tables"""

    connection = db_connection()
    cursor =connection.cursor()

    database = Database()
    queries = database.db_query()

    for sql in queries:        
        cursor.execute(sql)
        connection.commit()
        
    cursor.close()
