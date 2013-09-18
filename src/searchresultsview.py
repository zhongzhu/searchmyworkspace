from PySide import QtCore
from PySide import QtGui
from searchresultsmodel import SearchResultsModel
from searchresultsdelegate import SearchResultsDelegate

class SearchResultsView(QtCore.QObject):
       
    def __init__(self, myWidget):
        super(SearchResultsView, self).__init__(myWidget)
        self.myWidget = myWidget

        self.searchResultsModel = SearchResultsModel()
        self.myWidget.setModel(self.searchResultsModel)
        
        searchResultsDelegate = SearchResultsDelegate(self.myWidget)
        self.myWidget.setItemDelegate(searchResultsDelegate);

        self.myWidget.doubleClicked.connect(self.openViewer)

    def openViewer(self, index):
    	pass

    def clear(self):
    	self.searchResultsModel.clearMyModel()

    def handleSearchResults(self, docs):
        self.searchResultsModel.handleSearchResults(docs)
