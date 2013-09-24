import pysolr

class Updater(object):
    def __init__(self):
        self.solr = pysolr.Solr('http://localhost:8983/solr/myworkspace', timeout=10)

    def update(self, documents):
        """
        solr.add([
            {
                "id": "doc_1",
                "title": "A test document",
            },
            {
                "id": "doc_2",
                "title": "The Banana: Tasty or Dangerous?",
            },
        ])
        """
        self.solr.add(documents)
