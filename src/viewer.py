from PySide import QtCore
from PySide import QtGui
from testcaseviewer_ui import Ui_MainWindow_TestCaseViewer
from testasset import TestAsset, TestCase

def viewerSimpleFactory(fileLocation, parent = None):
    if fileLocation.endswith('.tc'):
        testAsset = TestCase(fileLocation)
        return TestCaseViewer(testAsset, parent)     

class Viewer(QtGui.QMainWindow):
    def __init__(self, testAsset, parent = None):
        super(Viewer, self).__init__(parent)
        self.testAsset = testAsset

    def showDetailedContent(self):
        pass

    def setContentToViewer(self, fileContent, highlighter):
        pass

class TestCaseViewer(Viewer, Ui_MainWindow_TestCaseViewer):
       
    def __init__(self, testAsset, parent = None):
        super(TestCaseViewer, self).__init__(testAsset, parent)
        self.setupUi(self)

    def showDetailedContent(self):
        fileLocation = self.testAsset.getFileLocation()
        if len(fileLocation) == 0:
            return

        self.setWindowTitle(fileLocation)

        try:
            fileContent = self.testAsset.getFileContent()
            highlighter = self.testAsset.setSyntaxHighlighter(self.textEdit_viewer.document())            
            self.setContentToViewer(fileContent, highlighter)
        except Exception, e:
            print(e)

        self.show()      

    def setContentToViewer(self, fileContent, highlighter):
        self.textEdit_viewer.setPlainText(fileContent)
                 