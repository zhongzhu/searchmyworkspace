from PySide import QtCore
from PySide import QtGui
from facetmodel import FacetModel

class FacetView(QtCore.QObject):
    facetOptionChanged = QtCore.Signal()
       
    def __init__(self, myWidget):
        super(FacetView, self).__init__(myWidget)
        self.myWidget = myWidget

        self.facetModel = FacetModel()
        self.myWidget.setModel(self.facetModel)

        self.facetModel.modelReset.connect(self.myWidget.expandAll)
        self.facetModel.facetOptionChanged.connect(self.facetOptionChanged)   

    def clear(self):
        self.facetModel.clearMyModel()

    def getFacetSearchOptions(self):
        return self.facetModel.getFacetSearchOptions()

    def handleSearchResults(self, facets):
        self.facetModel.handleSearchResults(facets)        