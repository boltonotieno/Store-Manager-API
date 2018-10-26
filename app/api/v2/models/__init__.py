import psycopg2
import os


url = os.getenv('DATABASE_URL')          

#creating the connection
con = psycopg2.connect(url)

#creating the cursor
cur = con.cursor()

con.close()
