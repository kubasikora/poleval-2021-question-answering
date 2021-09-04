from elasticsearch6 import Elasticsearch

class Document(object):
    def __init__(self, id, title, abstract, text):
        self.id       = id
        self.title    = title
        self.abstract = abstract
        self.text     = text

class Elastic(object):
    def __init__(self, url, index):
        self.elastic_url = url
        self.index = index
        self.es = Elasticsearch([url])

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
            try:
                id       = doc['_id']
                title    = doc['_source']['title']
                abstract = doc['_source']['opening_text']
                text     = doc['_source']['text']
                new_doc  = Document(id, title, abstract, text)
                documents.append(new_doc)
            except:
                pass
        return documents
