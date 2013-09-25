import pysolr
import utils.myconfig

class Updater(object):
    def __init__(self):
        self.config = utils.myconfig.MyConfig()

        solrURL = self.config.get('solr', 'solrURL')
        self.solr = pysolr.Solr(solrURL, timeout=10)

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
