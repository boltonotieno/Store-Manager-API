import psycopg2
import os
from ..models import db_connection

class Products:
    """Class contain product model functions"""

    connection = db_connection()
    cursor = connection.cursor()

    def create_table_products(self):
        """create Table products"""

        sql="""CREATE TABLE IF NOT EXISTS products(
        productid SERIAL PRIMARY KEY UNIQUE NOT NULL,
        name VARCHAR(50) NOT NULL,
        price INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        min_quantity INTEGER NOT NULL,
        category VARCHAR(15) NOT NULL
        )"""
        self.cursor.execute(sql)
        self.connection.commit()

    def drop_table_peoducts(self):
        """drop Table products"""

        sql="""DROP TABLE products"""
        self.cursor.execute(sql)
        self.connection.commit()

    def create_product(self):
        """creates a new product"""

        sql="""INSERT INTO products(name,price,quantity,min_quantity,category) VALUES(%s,%s,%s,%s,%s)"""

        return sql

    def get_all_products(self):
        """Fetch all products"""

        sql="SELECT * FROM products"
        
        return sql

    def get_one_product(self):
        """Fetch product by id"""

        sql="SELECT * FROM products WHERE productid = %s"
        return sql

    def modify_product(self):
        """modify a product"""

        sql="UPDATE products SET name = %s, price = %s, quantity = %s, min_quantity = %s, category = %s WHERE productid = %s"
        
        return sql

    def delete_product(self):
        """delete single products by id"""

        sql="DELETE FROM products WHERE productid = %s"

        return sql


