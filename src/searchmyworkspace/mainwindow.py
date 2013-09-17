from PySide import QtCore
from PySide import QtGui
from mainwindow_ui import Ui_MainWindow
from resultsmodel import SearchResultsModel
from facetmodel import FacetModel
from resultsdelegate import SearchResultsDelegate
from searcher import Searcher
import pysolr

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
       
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
                
        self.setupUi(self)

        self.setWindowTitle("Search My Workspace")

        # List to display search results
        self.searchResultsModel = SearchResultsModel()
        self.listView_result.setModel(self.searchResultsModel)

        searchResultsDelegate = SearchResultsDelegate(self.listView_result)
        self.listView_result.setItemDelegate(searchResultsDelegate);

        # Tree to display facets
        self.facetModel = FacetModel()
        self.treeView_facet.setModel(self.facetModel)
        self.facetModel.modelReset.connect(self.treeView_facet.expandAll)

        # searcher
        self.searcher = Searcher()
        self.searcher.searchDone.connect(self.searchDone)

        # signal slots
        self.createConnections()                

    ''' connect signal/slot pairs '''
    def createConnections(self):
        self.pushButton_search.clicked.connect(self.searchResultsModel.clearMyModel)
        self.pushButton_search.clicked.connect(self.facetModel.clearMyModel)
        self.pushButton_search.clicked.connect(self.search)

    def search(self):
        query = self.lineEdit_search.text()
        self.searcher.search(query)

    def searchDone(self):
        self.searchResultsModel.handleSearchResults(self.searcher.getDocs())
        self.facetModel.handleSearchResults(self.searcher.getFacets())
        self.label_searchResult.setText('About {0} search results for [{1}]'.format(self.searcher.getHits(), self.searcher.getQuery()))
