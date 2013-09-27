import os
import os.path
import time
import hashlib
import utils.updater
from testcase import testcase
from testcase import visitor
from tc2tet import Tc2Tet
import utils.myconfig
from progress.bar import Bar

def findTestCaseFile(path):
    for dirpath, dirs, files in os.walk(path):
        for file in files:
            fullName = os.path.join(dirpath, file)
            if os.path.splitext(fullName)[1] == '.tc':
                yield fullName

class MyUniqueKey(object):
    def getMyKey(self, type, content):
        return '{type}-{key}'.format(type=type, key=hashlib.md5(content).hexdigest())

class IndexerVisitor(visitor.Visitor):
    def __init__(self):
        pass

    def generateIndexDocument(self, indexDocument, tc):
        self.doc = indexDocument
        self.visit(tc.rootStep)

    def visit_StepTestCase(self, node):
        self.doc['tcid'] = node.data['tcid']
        self.doc['qcid'] = node.data['qcid']
        self.doc['title'] = node.data['title']
        self.doc['author'] = node.data['author']
        self.doc['created'] = node.data['created']
        self.doc['purpose'] = node.data['purpose']
        self.doc['usage'] = node.data['usage']

        #tag
        self.doc['tag'].append('easytest')

        #ne
        self.doc['ne'].append('HOST')

        for eachFunction in node.children:
            self.visit(eachFunction)

    def visit_StepFunction(self, node):
        self.doc['function'].append(node.data['name'])

        for eachStep in node.children:
            self.visit(eachStep)

    def visit_StepActionService(self, node):
        pass

    def visit_StepActionSimple(self, node):
        pass

    def visit_StepActionSession(self, node):
        pass

class Indexer(object):
    def __init__(self):
        self.keyGen = MyUniqueKey()
        self.indexerVisitor = IndexerVisitor()
        self.solr = utils.updater.Updater()

    def indexMyWorkspace(self, workspacePath):
        startTime = time.time()
        myFindTestCaseFile = findTestCaseFile(workspacePath)
        tcFiles = list(myFindTestCaseFile)
        print "Going to index {} test cases".format(len(tcFiles))

        # progresser = Bar('Indexing', max = len(tcFiles))
        for tcFile in tcFiles:
            print(tcFile)
            doc = self.indexOneTestCase(tcFile)
            # print doc
            self.solr.update([doc])
            # progresser.next()

        # progresser.finish()

    def indexOneTestCase(self, testCaseFilePath):
        tc = testcase.TestCase(testCaseFilePath)
        tc.load()

        tc2tet = Tc2Tet()

        doc = {}
        doc['id'] = self.keyGen.getMyKey('testcase', tc.tcFileName)
        doc['type'] = 'test case'
        doc['title'] = ''
        doc['tcid'] = ''
        doc['qcid'] = ''
        doc['tcname'] = tc.tcFileName
        doc['author'] = ''
        doc['created'] = ''
        doc['tag'] = []
        doc['purpose'] = ''
        doc['ne'] = []
        doc['usage'] = ''
        doc['function'] = []
        doc['content'] = tc2tet.transformFromTestCase(tc)
        doc['url'] = tc.tcFileName

        self.indexerVisitor.generateIndexDocument(doc, tc)

        return doc

if __name__ == '__main__':
    indexer = Indexer()
    config = utils.myconfig.MyConfig()
    folders = config.getList('solr', 'indexFolders')
    for folder in folders:
        indexer.indexMyWorkspace(folder)
