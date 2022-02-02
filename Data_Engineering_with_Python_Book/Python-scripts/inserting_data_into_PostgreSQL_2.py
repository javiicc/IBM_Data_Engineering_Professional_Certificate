import psycopg2 as db
from faker import Faker

fake = Faker()
data = []

for i in range(2, 1001):
    data.append((i, fake.name(), fake.street_address(), fake.city(), fake.zipcode()))

# Convert into a tuple of tuples
data_for_db = tuple(data)

conn_string = "dbname='dataengineering' " \
              "host='127.0.0.1' " \
              "user='postgres' " \
              "password='postgres'"
# Create a connection object
conn = db.connect(conn_string)
# Create the cursor
cur = conn.cursor()

query = "insert into users (id, name, street, city, zip) " \
        "values(%s,%s,%s,%s,%s)"

print(cur.mogrify(query, data_for_db[1]))

cur.executemany(query, data_for_db)
conn.commit()