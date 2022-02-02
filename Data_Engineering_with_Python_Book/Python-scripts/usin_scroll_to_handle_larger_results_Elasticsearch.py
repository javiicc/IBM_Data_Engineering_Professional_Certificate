from elasticsearch import Elasticsearch


# Create Elasticsearch instance
es = Elasticsearch()

response = es.search(
    index='users',
    scroll='20m',
    size=500,
    query={'match_all': {}}
)

sid = response['_scroll_id']
size = response['hits']['total']['value']

while size > 0:
    response = es.scroll(scroll_id=sid, scroll='20m')

sid = response['_scroll_id']
size = len(response['hits']['hits'])
print(size)

for doc in response['hits']['hits']:
    print(doc['_source'])
