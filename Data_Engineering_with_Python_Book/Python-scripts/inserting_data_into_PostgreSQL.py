import psycopg2 as db


conn_string = "dbname='dataengineering' " \
              "host='127.0.0.1' " \
              "user='postgres' " \
              "password='postgres'"

# Create a connection object
conn = db.connect(conn_string)
# Create the cursor
cur = conn.cursor()

#query = "insert into users (id, name, street, city, zip) " \
 #       "values({},'{}','{}','{}','{}')".format(1, 'Big Bird', 'Sesame Street',
  #                                               'Fakeville', '12345')

# cur.mogrify(query)

query2 = "insert into users (id, name, street, city, zip) " \
        "values(%s,%s,%s,%s,%s)"
data = (1, 'Big Bird', 'Sesame Street', 'Fakeville', '12345')

cur.mogrify(query2, data)

cur.execute(query2, data)

conn.commit()
