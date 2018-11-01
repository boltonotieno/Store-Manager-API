import psycopg2
import os
from ..models import db_connection


class Products:
    """Class contain product model functions"""

    connection = db_connection()
    cursor = connection.cursor()

    def create_table_products(self):
        """create Table products"""

        sql = """CREATE TABLE IF NOT EXISTS products(
        productid SERIAL PRIMARY KEY UNIQUE NOT NULL,
        name VARCHAR(50) UNIQUE NOT NULL,
        price INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        min_quantity INTEGER NOT NULL,
        categoryid INTEGER REFERENCES category(categoryid)
        )"""
        self.cursor.execute(sql)
        self.connection.commit()

    def drop_table_products(self):
        """drop Table products"""

        sql = """DROP TABLE products"""
        self.cursor.execute(sql)
        self.connection.commit()

    def create_product(self):
        """creates a new product"""

        sql = """INSERT INTO products(name,price,quantity,min_quantity,categoryid) \
        VALUES(%s,%s,%s,%s,%s)"""

        return sql

    def get_all_products(self):
        """Fetch all products"""

        sql = "SELECT * FROM products"
        
        return sql

    def get_one_product(self, product_id):
        """Fetch product by id"""

        sql = "SELECT * FROM products WHERE productid = %s"
        self.cursor.execute(sql, (product_id,))
        data = self.cursor.fetchone()

        return data

    def modify_product(self):
        """modify a product"""

        sql = "UPDATE products SET name = %s, price = %s, quantity = %s, min_quantity = %s, \
        categoryid = %s WHERE productid = %s"
        return sql

    def delete_product(self):
        """delete single products by id"""

        sql = "DELETE FROM products WHERE productid = %s"

        return sql

    def get_product__by_name(self, product_name):
        """get product name from db using product name"""

        sql = "SELECT * FROM products WHERE name = %s"
        self.cursor.execute(sql, (product_name,))
        data = self.cursor.fetchone()

        return data

    def get_product_price(self, product_name):
        """get product price using product name"""

        sql = "SELECT * FROM products WHERE name = %s"
        self.cursor.execute(sql, (product_name,))
        data = self.cursor.fetchone()

        return data[2]

    def get_product_quantity(self, product_name):
        """get product quantity using product name"""

        sql = "SELECT * FROM products WHERE name = %s"
        self.cursor.execute(sql, (product_name,))
        data = self.cursor.fetchone()

        return data[3]
 
    def get_product_min_quantity(self, product_name):
        """get product min_quantity using product name"""

        sql = "SELECT * FROM products WHERE name = %s"
        self.cursor.execute(sql, (product_name,))
        data = self.cursor.fetchone()

        return data[4]

    def reduce_product_quantity(self, new_quantity, product_name):
        """reduce product quantity after sale"""

        sql = "UPDATE products SET quantity = %s WHERE name = %s"
        self.cursor.execute(sql, (new_quantity, product_name,))
        self.connection.commit()

        