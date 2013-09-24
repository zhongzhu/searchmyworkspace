from PySide import QtCore
from PySide import QtGui
from highlighter import TestCaseHighlighter
from tc2tet import Tc2Tet

class TestAssetType(object):
    NONE = 0
    TESTCASE = 100
    SERVICE = 101
    LANGUAGE_REFERENCE = 102

class TestAsset(object):
    def __init__(self, fileLocation):
        self.fileLocation = fileLocation

    def getFileLocation(self):
        return self.fileLocation

    def getTestAssetType(self):
        return TestAssetType.NONE

    def getFileContent(self):
        pass

    def setSyntaxHighlighter(self, document):
        pass

class TestCase(TestAsset):
    def __init__(self, fileLocation):
        super(TestCase, self).__init__(fileLocation)

    def getTestAssetType(self):
        return TestAssetType.TESTCASE

    def setSyntaxHighlighter(self, document):
        TestCaseHighlighter(document)

    def getFileContent(self):
        tc2tet = Tc2Tet()
        return tc2tet.transform(self.fileLocation)
