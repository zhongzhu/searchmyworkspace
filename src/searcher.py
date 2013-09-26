import pysolr
from PySide import QtCore
import utils.myconfig

class Searcher(QtCore.QObject):
    """ Used to search Solr Index """
    searchDone = QtCore.Signal(int)

    def __init__(self):
        super(Searcher, self).__init__()
        self.query = ""
        self.results = None
        self.options = {'facet':'true','facet.field':['type','ne','tag','author'], 'facet.mincount':'1'}
        self.highLightOptions = {'hl':'true', 'hl.fragsize':'200',
            'hl.simple.pre':"<span style='background:yellow'>",
            'hl.simple.post':'</span>'}
        self.config = utils.myconfig.MyConfig()

        solrURL = self.config.get('solr', 'solrURL')
        self.solr = pysolr.Solr(solrURL, timeout=10)

    def search(self, query, userOptions = {}):
        if query == '':
            query = '*'
        self.query = query

        newOptions = dict(self.options, **userOptions)
        if self.query != '*':
            newOptions.update(self.highLightOptions)

        self.results = self.solr.search(self.query, **newOptions)
        self.searchDone.emit(len(self.results))

    def getDocs(self):
        if self.results:
            return self.results.docs
        else:
            return []

    def getHighlighting(self):
        if self.results:
            return self.results.highlighting
        else:
            return {}

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
