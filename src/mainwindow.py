from PySide import QtCore
from PySide import QtGui
from mainwindow_ui import Ui_MainWindow
from facetmodel import FacetModel
from searcher import Searcher
from facetview import FacetView
from searchresultsview import SearchResultsView
import viewer
import pysolr

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)

        self.setupUi(self)

        self.searchResultsView = SearchResultsView(self.listView_result)
        self.searchResultsView.viewDetailedContent.connect(self.showDetailedContent)

        self.facetView = FacetView(self.treeView_facet)
        self.facetView.facetOptionChanged.connect(self.search)

        # searcher
        self.searcher = Searcher()
        self.searcher.searchDone.connect(self.searchDone)

        self.createConnections()

    def createConnections(self):
        self.pushButton_search.clicked.connect(self.searchResultsView.clear)
        self.pushButton_search.clicked.connect(self.facetView.clear)
        self.pushButton_search.clicked.connect(self.search)

    def search(self):
        query = self.lineEdit_search.text()
        options = self.facetView.getFacetSearchOptions()
        self.searcher.search(query, options)

    def showDetailedContent(self, fileLocation):
        myviewer = viewer.viewerSimpleFactory(fileLocation, self)
        myviewer.showDetailedContent()

    @QtCore.Slot(int)
    def searchDone(self, searchResultCount):
        if searchResultCount > 0:
            self.searchResultsView.handleSearchResults(self.searcher.getDocs(), self.searcher.getHighlighting())
            self.facetView.handleSearchResults(self.searcher.getFacets())

        self.label_searchResult.setText('About {0} search results for [{1}]'.format(searchResultCount, self.searcher.getQuery()))
