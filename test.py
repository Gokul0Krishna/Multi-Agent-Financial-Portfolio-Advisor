import os
from dotenv import load_dotenv
import psycopg2

DB_PASSWORD = os.getenv('server_password')

# print(DB_PASSWORD)

conn = psycopg2.connect(
    dbname="postgres", user="postgres", password=DB_PASSWORD, host="localhost"
)
conn.autocommit = True
cur = conn.cursor()
print(cur.execute("SELECT version();"))
cur.close()
conn.close()