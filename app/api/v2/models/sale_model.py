import psycopg2
import os
from ..models import db_connection

class Sales:
    """Class contain sales model functions"""

    connection = db_connection()
    cursor = connection.cursor()

    def create_table_sales(self):
        """create Table sales"""

        sql="""CREATE TABLE IF NOT EXISTS sales(
        saleid SERIAL PRIMARY KEY UNIQUE NOT NULL,
        name VARCHAR(50) NOT NULL,
        price INTEGER NOT NULL,
        quantity INTEGER NOT NULL
        )"""
        self.cursor.execute(sql)
        self.connection.commit()

    def drop_table_sales(self):
        """drop Table sales"""

        sql="""DROP TABLE sales"""
        self.cursor.execute(sql)
        self.connection.commit()

    def create_sales(self):
        """creates a new sale"""

        sql="""INSERT INTO sales(name,price,quantity) VALUES(%s,%s,%s)"""

        return sql

    def get_all_sales(self):
        """Fetch all sales"""

        sql="SELECT name, price, quantity, price * quantity as total_amount FROM sales"
        
        return sql

    def get_one_sale(self):
        """Fetch sale by id"""

        sql="SELECT name, price, quantity, price * quantity as total_amount FROM sales WHERE saleid = %s"
        return sql

    def modify_sales(self):
        """modify a sales"""

        sql="UPDATE sales SET name = %s, price = %s, quantity = %s WHERE saleid = %s"
        
        return sql

    def delete_sales(self):
        """delete single sale by id"""

        sql="DELETE FROM sales WHERE saleid = %s"

        return sql

