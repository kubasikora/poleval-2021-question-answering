from elasticsearch6 import Elasticsearch

class Document(object):
    def __init__(self, title, abstract, text):
        self.title = title
        self.abstract = abstract
        self.text = text

class Elastic(object):
    def __init__(self, url, index):
        self.elastic_url = url
        self.index = index
        self.es = Elasticsearch([url], sniff_on_start=True, sniff_on_connection_fail=True)

    def get(self, query):
        res = self.es.search(
            index=self.index,
            body={
                'query': {
                    'multi_match': {
                        'query': query,
                        'fields': ['title', 'text']
                    }
                }
            }
        )
        items = res['hits']['hits']
        documents = []
        for doc in items:
            title    = doc['_source']['title']
            abstract = doc['_source']['opening_text']
            text     = doc['_source']['text']
            new_doc  = Document(title, abstract, text)
            documents.append(new_doc)
        return documents
