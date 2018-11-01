import psycopg2
import os
from ..models import db_connection
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_claims,
    get_jwt_identity)


class Users:
    """Class contain user model functions"""

    connection = db_connection()
    cursor = connection.cursor()

    def create_table_user(self):
        """create Table users"""

        sql = """CREATE TABLE IF NOT EXISTS users(
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

        sql = """DROP TABLE users"""
        self.cursor.execute(sql)
        self.connection.commit()

    def register_user(self):
        """creates a new user"""

        sql = """INSERT INTO users(name,username,email,password,gender,role)\
         VALUES(%s,%s,%s,%s,%s,%s)"""

        return sql

    def get_all_users(self):
        """Fetch all users"""

        sql = "SELECT * FROM users"

        return sql

    def get_one_user(self):
        """Fetch user by id"""

        sql = "SELECT * FROM users WHERE userid = %s"
        return sql

    def get_one_user_username(self):
        """Fetch user by username"""

        sql = "SELECT * FROM users WHERE username = %s"
        return sql

    def get_user_by_username(self):
        """Fetch user by username"""

        sql = "SELECT password FROM users WHERE username = %s"
        return sql

    def get_username(self):
        current_user = get_jwt_identity()
        sql = "SELECT role FROM users WHERE username = %s"
        self.cursor.execute(sql, (current_user,))
        role = self.cursor.fetchone()
        return role

    def get_user_role(self):
        """Fetch user role"""
        current_user = get_jwt_identity()
        sql = "SELECT role FROM users WHERE username = %s"
        self.cursor.execute(sql, (current_user,))
        role = self.cursor.fetchone()
        return role

    def modify_user_role(self, new_role, user_id):
        """modify a user role"""

        sql = "UPDATE users SET role = %s WHERE userid = %s"
        self.cursor.execute(sql, (new_role, user_id))
        self.connection.commit()
        
