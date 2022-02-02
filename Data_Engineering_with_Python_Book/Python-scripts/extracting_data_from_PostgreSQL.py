import psycopg2 as db


conn_string = "dbname='dataengineering' " \
              "host='127.0.0.1' " \
              "user='postgres' " \
              "password='postgres'"
# Create a connection object
conn = db.connect(conn_string)
# Create the cursor
cur = conn.cursor()

query = "select * from users"
cur.execute(query)

# for record in cur:
 #   print(record)

# cur.fetchall()
# cur.fetchmany(5)
# cur.fetchone()

data = cur.fetchall()
# print(data[0])

# cur.rowcount
# 1001
# cur.rownumber

file = open('../../../fromdb.csv', 'w')
cur.copy_to(file, 'users', sep=',')
file.close()
