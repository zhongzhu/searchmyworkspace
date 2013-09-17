from PySide import QtCore
from PySide import QtGui

class FacetTreeView(QtGui.QTreeView):
       
    def __init__(self, parent = None):
        super(FacetTreeView, self).__init__(parent)