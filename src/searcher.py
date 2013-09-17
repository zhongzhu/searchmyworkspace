import pysolr
from PySide import QtCore

class Searcher(QtCore.QObject):
    """ Used to search Solr Index """
    searchDone = QtCore.Signal(int)

    def __init__(self):
        super(Searcher, self).__init__()
        self.query = ""
        self.results = None       
        self.options = {'facet':'true', 'facet.field':['type','ne','tag','author'], 'facet.mincount':'1'} 
        self.solr = pysolr.Solr('http://localhost:8983/solr/myworkspace', timeout=10)

    def search(self, query, userOptions = {}):
        self.query = query
        newOptions = dict(self.options, **userOptions)

        self.results = self.solr.search(self.query, **newOptions)
        self.searchDone.emit(len(self.results))

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