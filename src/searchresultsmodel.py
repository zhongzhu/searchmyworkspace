from PySide import QtCore
from PySide import QtGui
from roles import ResultRoles

class SearchResultsModel(QtCore.QAbstractListModel):
    # facetDataReady = QtCore.Signal(dict)

    def __init__(self, parent=None):
        super(SearchResultsModel, self).__init__(parent)
        self.docs = []

    def clearMyModel(self):
        self.docs = []
        self.reset()

    def handleSearchResults(self, docs, highlightings):
        self._updateDocWithHighlight(docs, highlightings)
        self.docs = docs
        self.reset()

    def getUrl(self, index):
        return self.docs[index.row()]["url"]

    def data(self, index, role):
        if not index.isValid():
            return None

        if index.row() >= len(self.docs):
            return None

        if role == QtCore.Qt.DisplayRole:
            return self.docs[index.row()]["tcname"]
        elif role == ResultRoles.TypeRole:
            return self.docs[index.row()]["type"]
        elif role == ResultRoles.AuthorRole:
            return self.docs[index.row()]["author"]
        elif role == ResultRoles.DateRole:
            return self.docs[index.row()]["created"]
        elif role == ResultRoles.TitleRole:
            return self.docs[index.row()]["tcname"]
        elif role == ResultRoles.PreviewContentRole:
            return self.docs[index.row()]["content"]
        else:
            return None

    def rowCount(self, parent):
        return len(self.docs)

    def _updateDocWithHighlight(self, docs, highlightings):
        if len(highlightings) > 0:
            for doc in docs:
                doc['content'] = highlightings[doc['id']]['content'][0]
