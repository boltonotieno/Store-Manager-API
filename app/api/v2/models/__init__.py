import psycopg2
import os
from .database_model import Database


def db_connection():
    """Create Database Connection"""

    url = "dbname='store_manager' host='localhost' \
     port='5432' user='postgres'"

    # url = "dbname='test_store_manager' host='localhost' port='5432' \
    #  user='bolt'password='root123!'"
     
    # url = os.getenv('DATABASE_URL')
    connection = psycopg2.connect(url)
    return connection


def create_tables():
    """Creates the Tables"""

    connection = db_connection()
    cursor = connection.cursor()

    database = Database()
    queries = database.db_query()

    for sql in queries:        
        cursor.execute(sql)
        connection.commit()
        
    cursor.close()


def create_default_admin():
    connection = db_connection()
    cursor = connection.cursor()

    name = 'default admin'
    username = 'admin'
    email = 'admin@gmail.com'
    password = 'adminpass'
    gender = 'male'
    role = 'admin'

    sql = "SELECT * FROM users WHERE username = %s"
    cursor.execute(sql, (username,))
    data = cursor.fetchone()

    if not data:
        sql = 'INSERT INTO users(name,username,email,password,gender,role) \
         VALUES(%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql, (name, username, email, password, gender, role))
        connection.commit()
        connection.close()


def drop_tables():
    connection = db_connection()
    cursor = connection.cursor()

    database = Database()
    queries = database.drop_query()

    for sql in queries:        
        cursor.execute(sql)
        connection.commit()
    