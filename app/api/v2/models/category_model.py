import psycopg2
import os
from ..models import db_connection

class Categories:
    """Class contain category model functions"""

    connection = db_connection()
    cursor = connection.cursor()

    def create_table_category(self):
        """create Table category"""

        sql="""CREATE TABLE IF NOT EXISTS category(
        categoryid SERIAL PRIMARY KEY UNIQUE NOT NULL,
        name VARCHAR(50) UNIQUE NOT NULL
        )"""
        self.cursor.execute(sql)
        self.connection.commit()

    def drop_table_category(self):
        """drop Table category"""

        sql="""DROP TABLE category CASCADE"""
        self.cursor.execute(sql)
        self.connection.commit()

    def create_category(self):
        """creates a new category"""

        sql="""INSERT INTO category(name) VALUES(%s)"""

        return sql

    def get_all_category(self):
        """Fetch all categories"""

        sql="SELECT * FROM category"
        
        return sql

    def get_one_category(self, category_id):
        """Fetch category by id"""

        sql="SELECT * FROM category WHERE categoryid = %s"
        self.cursor.execute(sql,(category_id,))
        data = self.cursor.fetchone()

        return data


    def modify_category(self):
        """modify a category"""

        sql="UPDATE category SET name = %s WHERE categoryid = %s"
        
        return sql

    def delete_category(self):
        """delete single category by id"""

        sql="DELETE FROM category WHERE categoryid = %s"

        return sql
    
    def get_category__by_name(self, category_name):
        """get category name from db using category name"""

        sql="SELECT * FROM category WHERE name = %s"
        self.cursor.execute(sql,(category_name,))
        data = self.cursor.fetchone()

        return data

