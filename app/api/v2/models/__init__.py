import psycopg2
import os


def db_connection:
    """Create Database Connection"""

    url = os.getenv('DATABASE_URL')          
    connection = psycopg2.connect(url)

    return connection

# creating the cursor
# cur = con.cursor()

