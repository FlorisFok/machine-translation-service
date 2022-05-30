from opensearchpy import OpenSearch
import os
import json

WEBHOOK = os.getenv('WEBHOOK', '')

def send_(mes):
    # Only use if there is a webhook
    if WEBHOOK == '':
        return

    #actual code for sending
    requests.post('https://' + WEBHOOK, 
                    headers={'Content-Type': 'application/json',}, 
                    data='{ "username":"check_bot", "text": \"' + mes +'\"}')

class ElasticStorage():
    database =  'webapp_metrics'

    def __init__(self):
        DB_HOST = os.getenv('DB_HOST', "localhost")
        USER = os.getenv('OSUSER', "admin")
        PASS = os.getenv('OSPASS', "admin")

        # Connect client
        self.client = OpenSearch(
            hosts = [{'host': DB_HOST, 'port': 9200}],
            http_compress = True, # enables gzip compression for request bodies
            http_auth = ('admin', 'admin')
        )

    def store(self, document):
        """Save to OS"""
        # Send to database
        self.client.index(
            index =self.database,
            body = document,
            refresh = True
        )

    def bulk_store(self, index: str, payload=[], method: str = 'add'):
        """Save to OS but in bulk"""
        if method == 'add':
            bulks = ['{ "index" : { "_index" : \"' + index + '\"} } \n' +  json.dumps(doc) for doc in payload]

        elif method == "delete":
            bulks = ['{"delete":{"_id":\"' + i + '\"}}' for i in payload]

        return self.client.bulk('\n'.join(bulks), index=index, refresh=True)