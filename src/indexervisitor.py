
from testcase import testcase
from testcase import visitor
from tc2tet import Tc2Tet
import hashlib

class MyUniqueKey(object):
    def getMyKey(self, type, content):
        return '{type}-{key}'.format(type=type, key=hashlib.md5(content).hexdigest())

class IndexerVisitor(visitor.Visitor):
    def __init__(self):
        self.tc2tet = Tc2Tet()
        self.keyGen = MyUniqueKey()
        self.doc = {}

    def generateIndexDocument(self, testCaseFilePath):
        tc = testcase.TestCase(testCaseFilePath)
        tc.load()

        self.doc.clear()
        self.doc['id'] = self.keyGen.getMyKey('testcase', tc.tcFileName)

        self.doc['type'] = 'test case'
        self.doc['title'] = ''
        self.doc['tcid'] = ''
        self.doc['qcid'] = ''
        self.doc['tcname'] = tc.tcFileName
        self.doc['author'] = ''
        self.doc['created'] = ''
        self.doc['tag'] = []
        self.doc['purpose'] = ''
        self.doc['ne'] = []
        self.doc['usage'] = ''
        self.doc['function'] = []
        self.doc['content'] = self.tc2tet.transformFromTestCase(tc)
        self.doc['url'] = tc.tcFileName

        self.visit(tc.rootStep)

        return self.doc

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

if __name__ == '__main__':
    v = IndexerVisitor()
    doc = v.generateIndexDocument('D:\\EasyTest\\workspace\\tc\\service\\MS_LTE\\MS_LTE_aidaGetMobilesListFromAida.tc')
    print(doc)
