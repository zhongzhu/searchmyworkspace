from PySide.QtCore import *
from PySide.QtGui import *
from tccodehighlighter import Highlighter
from roles import ResultRoles

class MyItemSize(object):
    # size for displayed items
    MarginSize = 8
    PreviewWindowHeight = 100    
    TitleHeight = 20 
    DescriptionHeight = 20
    MyHeight = MarginSize * 2 + TitleHeight + DescriptionHeight + PreviewWindowHeight

class SearchResultsDelegate(QStyledItemDelegate):

    def __init__(self, parent=None):
        super(SearchResultsDelegate, self).__init__(parent)

    def sizeHint(self, option, index):
        """ Returns the size needed to display the item in a QSize object. """
        return QSize(option.rect.width(),  MyItemSize.MyHeight)

    def paint(self, painter, option, index):
        """
        *** ITEM LAYOUT
        +----------------------------------------------------------+
        |                          margin                          |
        +-+------------------------------------------------------+-+
        | |                      tc title                        | |
        |M|------------------------------------------------------|M|
        | |                      description                     | |
        | |------------------------------------------------------| |        
        | |                      preview window                  | | M = Margin
        +-+------------------------------------------------------+-+
        |                          margin                          |
        +----------------------------------------------------------+
        """

        if not index.isValid():
            pass

        # selected = option.state & QStyle.State_Selected
        # if selected:
        #     QStyledItemDelegate.paint(self, painter,option,index)

        # QApplication.style().drawPrimitive(QStyle.PE_PanelItemViewItem, option, painter)

        # tc title
        titleRect = QRect()
        titleRect.setX(option.rect.x() + MyItemSize.MarginSize)
        titleRect.setY(option.rect.y() + MyItemSize.MarginSize)
        titleRect.setWidth(option.rect.width() - MyItemSize.MarginSize * 2)
        titleRect.setHeight(MyItemSize.TitleHeight)

        title = index.data(ResultRoles.TitleRole)
        
        painter.save()
        f = QFont()
        f.setBold(True)
        f.setPointSize(12)        
        painter.setFont(f)    
        painter.setPen(QPen(Qt.blue))        
        fontMetrics = QFontMetrics(f)
        painter.drawText(titleRect, Qt.AlignLeft | Qt.AlignTop, fontMetrics.elidedText(title, Qt.ElideRight, titleRect.width()))
        painter.restore()

        # Description: Type:test case | Author: zhu@haha.com | Date: Sept. 11, 2010
        descriptionRect = QRect()
        descriptionRect.setX(option.rect.x() + MyItemSize.MarginSize)
        descriptionRect.setY(option.rect.y() + MyItemSize.MarginSize + MyItemSize.TitleHeight)
        descriptionRect.setWidth(option.rect.width() - MyItemSize.MarginSize * 2)
        descriptionRect.setHeight(MyItemSize.DescriptionHeight)

        description = "Type: {0} | Author: {1} | Date: {2}".format(index.data(ResultRoles.TypeRole), index.data(ResultRoles.AuthorRole), index.data(ResultRoles.DateRole))
        painter.save()
        descriptionFont = QFont()
        painter.setFont(descriptionFont)    
        painter.setPen(QPen(Qt.darkGray))
        fontMetrics = QFontMetrics(descriptionFont)
        painter.drawText(descriptionRect, Qt.AlignLeft | Qt.AlignTop, fontMetrics.elidedText(description, Qt.ElideRight, descriptionRect.width()))
        painter.restore()        

        # Preview window
        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(10)

        previewWindow = QTextEdit()
        previewWindow.setFont(font)
        previewWindow.resize(option.rect.width() - MyItemSize.MarginSize * 2, MyItemSize.PreviewWindowHeight)

        highlighter = Highlighter(previewWindow.document())       
        previewWindow.setPlainText(index.data(ResultRoles.PreviewContentRole))

        pixmap = QPixmap(previewWindow.size())        
        previewWindow.render(pixmap)

        previewWindowRect = QRect(option.rect.x() + MyItemSize.MarginSize, 
                                option.rect.y() + MyItemSize.MarginSize + MyItemSize.TitleHeight + MyItemSize.DescriptionHeight, 
                                previewWindow.width() - MyItemSize.MarginSize * 2, 
                                previewWindow.height())
        painter.drawPixmap(previewWindowRect, pixmap)
