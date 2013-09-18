from PySide import QtCore
from PySide import QtGui

class FacetTreeView(QtCore.QObject):
       
    def __init__(self, myWidget):
        super(FacetTreeView, self).__init__(myWidget)
        self.myWidget = myWidget