from PySide import QtCore

class TreeItem(object):
    FACET_NAME = 0
    FACET_VALUE = 1
    def __init__(self, data, isLeaf = True, isChecked = False, parent=None):
        self.parentItem = parent
        #('test case', 2)
        self.itemData = data
        self.checked = isChecked
        self.isLeaf = isLeaf
        self.childItems = []

    def getMyName(self):
        return self.itemData[TreeItem.FACET_NAME]

    def getMyValue(self):
        return self.itemData[TreeItem.FACET_VALUE]        

    def setChecked(self, checked):
        self.checked = checked

    def appendChild(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return len(self.itemData)

    def data(self, role):
        if QtCore.Qt.CheckStateRole == role:
            if self.isLeaf:
                if self.checked:
                    return QtCore.Qt.Checked
                else:
                    return QtCore.Qt.Unchecked
        elif QtCore.Qt.DisplayRole == role:
            if self.isLeaf:
                return "{0} ({1})".format(self.getMyName(), self.getMyValue()) 
            else:
                return self.getMyName()
        else:
            return None       

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)

        return 0

class FacetSearchOptions(object):
    def __init__(self):
        super(FacetSearchOptions, self).__init__()
        self.options = set()

    def updateOption(self, facetFieldName, facetName, isToAdd = True):
        # 'fq':['ne:("RNC")' ,'ne:("HOST")']
        option = '{0}:("{1}")'.format(facetFieldName, facetName)
        if isToAdd:
            self.options.add(option)
        else:
            if option in self.options:
                self.options.remove(option)

    def getOptions(self):
        if len(self.options) > 0:
            return dict({'fq':list(self.options)})        
        else:
            return {}

    def clear(self):
        self.options.clear()

    def thisFacetNameWasSelected(self, facetFieldName, facetName):
        option = '{0}:("{1}")'.format(facetFieldName, facetName)
        if option in self.options:
            return True
        else:
            return False

class FacetModel(QtCore.QAbstractItemModel):
    facetOptionChanged = QtCore.Signal()

    def __init__(self, parent=None):
        super(FacetModel, self).__init__(parent)
        self.rootItem = TreeItem(("Facet"), False, False, None)
        self.facetSearchOptions = FacetSearchOptions()

    def thisFacetNameWasSelected(self, facetFieldName, facetName):
        return self.facetSearchOptions.thisFacetNameWasSelected(facetFieldName, facetName)

    def getFacetSearchOptions(self):
        return self.facetSearchOptions.getOptions()

    def clearMyModel(self):
        self.rootItem = TreeItem(("Facet"), False, False, None)
        self.facetSearchOptions.clear()
        self.reset()              

    def columnCount(self, parent):
        return 1
        
    def data(self, index, role):
        if not index.isValid():
            return None

        item = index.internalPointer()

        return item.data(role)

    def setData(self, index, value, role):
        if not index.isValid():
            return False

        item = index.internalPointer()
        if QtCore.Qt.CheckStateRole == role:
            item.setChecked(value)
            self.dataChanged.emit(index, index)

            self.facetSearchOptions.updateOption(item.parentItem.getMyName(), item.getMyName(), value)
            self.facetOptionChanged.emit()
            return True
        else:
            return False

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.NoItemFlags

        item = index.internalPointer()
        if item.isLeaf:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable
        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable            

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return "Refine your search results"

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()      

    def handleSearchResults(self, facets):
        """
        author
          +----henry zhong (2)
          +----Jack london (1) 
        tag
          +----sanity (1)
          +----feature (2) 
        """
        self.rootItem = TreeItem(("Facet"), False, False, None)

        facet_fields = facets.get('facet_fields')
        for facetFieldName in facet_fields.keys():
            facetFieldItem = TreeItem((facetFieldName, None), False, False, self.rootItem)
            self.rootItem.appendChild(facetFieldItem)

            #["a",1,"b",2] -> [("a",1),("b",2)]
            facetNameAndValueTupleList = zip(*[iter(facet_fields[facetFieldName])]*2)
            for facetNameAndValueTuple in facetNameAndValueTupleList:
                facetFieldItem.appendChild(
                    TreeItem(facetNameAndValueTuple, True, 
                        self.thisFacetNameWasSelected(facetFieldName, facetNameAndValueTuple[0]), 
                        facetFieldItem))

        self.reset()
