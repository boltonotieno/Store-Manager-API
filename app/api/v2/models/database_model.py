
class Database():
    """Database class"""
    def db_query(self):
        query_users="""CREATE TABLE IF NOT EXISTS users(
            userid SERIAL PRIMARY KEY UNIQUE NOT NULL,
            name VARCHAR(50) NOT NULL,
            username VARCHAR(50) NOT NULL UNIQUE,
            email VARCHAR(150) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            gender VARCHAR(15) NOT NULL,
            role VARCHAR(15) NOT NULL
            )"""

        query_category="""CREATE TABLE IF NOT EXISTS category(
            categoryid SERIAL PRIMARY KEY UNIQUE NOT NULL,
            name VARCHAR(50) UNIQUE NOT NULL
            )"""

        query_products="""CREATE TABLE IF NOT EXISTS products(
            productid SERIAL PRIMARY KEY UNIQUE NOT NULL,
            name VARCHAR(50) UNIQUE NOT NULL,
            price INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            min_quantity INTEGER NOT NULL,
            category VARCHAR(15) NOT NULL
            )"""

        query_sales="""CREATE TABLE IF NOT EXISTS sales(
            saleid SERIAL PRIMARY KEY UNIQUE NOT NULL,
            name VARCHAR(50) NOT NULL,
            price INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            attendant VARCHAR(10) NOT NULL
            )"""

        self.query =[query_users,query_category,query_products,query_sales]
        
        return self.query

