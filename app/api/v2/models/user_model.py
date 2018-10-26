import psycopg2
from . import db_connection

class Users(object):
    """Class contain user model functions"""

    def create_table_user(self, connection):
        """create Table users"""

        sql="""CREATE TABLE IF NOT EXISTS users(
        userid SERIAL PRIMARY KEY UNIQUE NOT NULL,
        name VARCHAR(25) NOT NULL,
        username VARCHAR(50) NOT NULL UNIQUE,
        email VARCHAR(150) NOT NULL UNIQUE,
        password VARCHAR(25) NOT NULL,
        gender VARCHAR(5) NOT NULL
        )"""
        cursor = connection.cursor()
        cursor.execute(sql)

    def register_user(self, name,username,email,password,gender):
        """creates a new user"""

        sql="""INSERT INTO users(name,username,email,password,gender) VALUES(%s,%s,%s,%s,%s)"""
        cursor.execute(sql,(name,username,email,password,gender))
        return cursor

    def get_all_users(self):
        """Fetch all users"""

        sql="SELECT * FROM users"
        cursor.execute(sql)
        return cursor

    def get_one_user(self,userid):
        """Fetch user by id"""

        sql="SELECT * FROM users WHERE userid = %s"
        cursor.execute(sql,(userid,))
        return cursor
