from PySide import QtCore

class TreeItem(object):
    def __init__(self, data, isLeaf = True, parent=None):
        self.parentItem = parent
        self.itemData = data
        self.checked = False
        self.isLeaf = isLeaf
        self.childItems = []

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

    # def data(self, column):
    #     try:
    #         return self.itemData[column]
    #     except IndexError:
    #         return None

    def data(self, role):
        if QtCore.Qt.CheckStateRole == role:
            if self.isLeaf:
                if self.checked:
                    return QtCore.Qt.Checked
                else:
                    return QtCore.Qt.Unchecked
        elif QtCore.Qt.DisplayRole == role:
            if self.isLeaf:
                return "{0} ({1})".format(self.itemData[0], self.itemData[1]) 
            else:
                return self.itemData[0]
        else:
            return None       

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)

        return 0

class FacetModel(QtCore.QAbstractItemModel):
    def __init__(self, parent=None):
        super(FacetModel, self).__init__(parent)
        self.rootItem = TreeItem(("Facet"), False, None)  

    def clearMyModel(self):
        self.rootItem = TreeItem(("Facet"), False, None)
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
            self.dataChanged.emit(index, index);
            print(item.data(QtCore.Qt.DisplayRole))
            return True

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
            return "Categories"

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
        facet_fields = facets.get('facet_fields')
        for oneFacetField in facet_fields.keys():
            oneFacetItem = TreeItem((oneFacetField, None), False, self.rootItem)
            self.rootItem.appendChild(oneFacetItem)

            #["a",1,"b",2] -> [("a",1),("b",2)]
            keywordAndCount = facet_fields[oneFacetField]            
            keywordAndCountTuples = zip(*[iter(keywordAndCount)]*2)
            for eachKeywordAndCountTuple in keywordAndCountTuples:
                oneFacetItem.appendChild(TreeItem(eachKeywordAndCountTuple, True, oneFacetItem))

        self.reset()
