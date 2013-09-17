import pysolr
from PySide import QtCore

class Searcher(QtCore.QObject):
    """ Used to search Solr Index """
    searchDone = QtCore.Signal()

    def __init__(self):
        super(Searcher, self).__init__()
        self.query = ""
        self.results = None       
        self.options = {'facet':'true', 'facet.field':['type','ne','tag','author'], 'facet.mincount':'1'} 

    def search(self, query, option = {}):
        self.query = query
        self.results = None
        solr = pysolr.Solr('http://localhost:8983/solr/mytc', timeout=10)
        newOptions = dict(self.options, **option)

        self.results = solr.search(self.query, **newOptions)
        if len(self.results) > 0:
            self.searchDone.emit()

    def getDocs(self):
        if self.results:
            return self.results.docs
        else:
            return []     

    def getFacets(self):
        if self.results:
            return self.results.facets
        else:
            return []                      
            
    def getHits(self):
        if self.results:
            return self.results.hits
        else:
            return 0         

    def getQuery(self):
        return self.query                  