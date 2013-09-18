from PySide import QtCore
from PySide import QtGui
from searchresultsmodel import SearchResultsModel
from searchresultsdelegate import SearchResultsDelegate

class SearchResultsView(QtCore.QObject):
    viewDetailedContent = QtCore.Signal(str)
       
    def __init__(self, myWidget):
        super(SearchResultsView, self).__init__(myWidget)
        self.myWidget = myWidget

        self.searchResultsModel = SearchResultsModel()
        self.myWidget.setModel(self.searchResultsModel)
        
        searchResultsDelegate = SearchResultsDelegate(self.myWidget)
        self.myWidget.setItemDelegate(searchResultsDelegate);

        self.myWidget.doubleClicked.connect(self.openViewer)

    def openViewer(self, index):
        if not index.isValid():
            return

        url = self.searchResultsModel.getUrl(index)
        if len(url) > 0:
            self.viewDetailedContent.emit(url)

    def clear(self):
    	self.searchResultsModel.clearMyModel()

    def handleSearchResults(self, docs):
        self.searchResultsModel.handleSearchResults(docs)
