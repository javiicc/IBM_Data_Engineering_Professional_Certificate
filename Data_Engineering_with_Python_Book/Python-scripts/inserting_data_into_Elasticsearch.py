from elasticsearch import Elasticsearch, helpers
from faker import Faker


# print(elasticsearch.__version__)

fake = Faker()

# Create connection to Elasticsearch
es = Elasticsearch({'127.0.0.1'})

doc = {
    'name': fake.name(),
    'street': fake.street_address(),
    'city': fake.city(),
    'zip': fake.zipcode()
}

response = es.index(index='users', document=doc)
print(response['result'])
print(es.info())

actions = [
    {
        '_op_type': 'index',
        '_index': 'users',
        '_source': {
            'name': fake.name(),
            'street': fake.street_address(),
            'city': fake.city(),
            'zip': fake.zipcode()
        }
    } for x in range(998)
]
# print(actions)

# response = helpers.bulk(es, actions)
# print(response)
# print(response[1])
try:
    # Make the bulk call, and get a response
    response = helpers.bulk(client=es, actions=actions, index='users')
    print ("\nRESPONSE:", response)
except Exception as e:
    print("\nERROR:", e)

