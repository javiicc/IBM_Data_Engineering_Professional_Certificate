import psycopg2 as db
import pandas as pd


conn_string = "dbname='dataengineering' " \
              "host='127.0.0.1' " \
              "user='postgres' " \
              "password='postgres'"
# Create a connection object
conn = db.connect(conn_string)

df = pd.read_sql("select * from users", conn)

df.to_json('../../../fromdb.json', orient='records')
