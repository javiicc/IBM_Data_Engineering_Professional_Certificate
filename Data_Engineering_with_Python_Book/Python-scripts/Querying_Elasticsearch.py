from elasticsearch import Elasticsearch
from pandas import json_normalize


# Create Elasticsearch instance
es = Elasticsearch()

response = es.search(index='users', size=10, query={'match_all': {}})
# print(response['hits']['hits'])
# print(len(response['hits']['hits']))
print(response['hits']['hits'][0]['_source'])

# for doc in response['hits']['hits']:
#     print(doc['_source'])

# df = json_normalize(response['hits']['hits'])
# print(df.head())

response = es.search(index='users', size=10, query={'match': {'name': 'Casey Brown'}})
print(response['hits']['hits'])

# response = es.search(index='users', size=10, q="name:'Casey Brown'")
# print(response['hits']['hits'][0]['_source'])

response = es.search(index='users', size=10, query={'match': {'city': 'Jamesberg'}})
print(response['hits']['hits'])

response = es.search(index='users', size=10,
                     query={'bool': {
                         'must': {'match': {'city': 'Jamesberg'}},
                         'filter': {'term': {'zip': '07293'}}
                     }})
print(response['hits']['hits'])
