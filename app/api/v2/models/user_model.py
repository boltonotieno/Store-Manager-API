import psycopg2
import os
from ..models import db_connection

class Users:
    """Class contain user model functions"""

    connection = db_connection()
    cursor = connection.cursor()

    def create_table_user(self):
        """create Table users"""

        sql="""CREATE TABLE IF NOT EXISTS users(
        userid SERIAL PRIMARY KEY UNIQUE NOT NULL,
        name VARCHAR(50) NOT NULL,
        username VARCHAR(50) NOT NULL UNIQUE,
        email VARCHAR(150) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        gender VARCHAR(15) NOT NULL,
        role VARCHAR(15) NOT NULL
        )"""
        self.cursor.execute(sql)
        self.connection.commit()

    def drop_table_user(self):
        """drop Table users"""

        sql="""DROP TABLE users"""
        self.cursor.execute(sql)
        self.connection.commit()

    def register_user(self):
        """creates a new user"""

        sql="""INSERT INTO users(name,username,email,password,gender,role) VALUES(%s,%s,%s,%s,%s,%s)"""

        return sql

    def get_all_users(self):
        """Fetch all users"""

        sql="SELECT * FROM users"
    
        return sql

    def get_one_user(self):
        """Fetch user by id"""

        sql="SELECT * FROM users WHERE userid = %s"
        return sql

    def get_user_by_username(self):
        """Fetch user by username"""

        sql="SELECT password FROM users WHERE username = %s"
        return sql


