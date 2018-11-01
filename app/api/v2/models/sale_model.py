import psycopg2
import os
from ..models import db_connection
from flask_jwt_extended import (create_access_token, jwt_required,
                                get_jwt_claims, get_jwt_identity)


class Sales:
    """Class contain sales model functions"""

    connection = db_connection()
    cursor = connection.cursor()

    def create_table_sales(self):
        """create Table sales"""

        sql = """CREATE TABLE IF NOT EXISTS sales(
        saleid SERIAL PRIMARY KEY UNIQUE NOT NULL,
        name VARCHAR(50) NOT NULL,
        price INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        attendant VARCHAR(10) NOT NULL
        )"""
        self.cursor.execute(sql)
        self.connection.commit()

    def drop_table_sales(self):
        """drop Table sales"""

        sql = """DROP TABLE sales"""
        self.cursor.execute(sql)
        self.connection.commit()

    def create_sales(self):
        """creates a new sale"""

        sql = """INSERT INTO sales(name,price,quantity,attendant)\
         VALUES(%s,%s,%s,%s)"""

        return sql

    def get_all_sales(self):
        """Fetch all sales"""

        sql = "SELECT saleid, name, price, quantity, attendant,\
        price * quantity as total_amount FROM sales"
        return sql

    def get_attendant_all_sales(self):
        """Fetch all sales for an attendant"""

        current_user = get_jwt_identity()
        sql = "SELECT saleid, name, price, quantity, attendant,\
         price * quantity as total_amount FROM sales WHERE attendant = %s"
        self.cursor.execute(sql, (current_user,))
        sale = self.cursor.fetchall()
        return sale

    def get_one_sale(self, sale_id):
        """Fetch sale by id"""

        sql = "SELECT saleid, name, price, quantity, attendant,\
         price * quantity as total_amount FROM sales WHERE saleid = %s"
        self.cursor.execute(sql, (sale_id,))
        data = self.cursor.fetchone()
        return data

    def modify_sales(self):
        """modify a sales"""

        sql = "UPDATE sales SET name = %s, price = %s,\
         quantity = %s WHERE saleid = %s"
        return sql

    def delete_sales(self):
        """delete single sale by id"""

        sql = "DELETE FROM sales WHERE saleid = %s"
        return sql

    def get_attendant_from_sales(self):
        """Fetch attendant username from sale"""

        sql = "SELECT attendant FROM sales WHERE saleid = %s"
        return sql
