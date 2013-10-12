'''
Created on Feb 8, 2012

@author: zhzhong
'''

from xml.dom import minidom
from xml.dom.minidom import *
import re

class StepType:
    STEP = 0
    STEP_TESTCASE = 1000
    STEP_FUNCTION = 2000
    STEP_ACTION = 3000
    STEP_ACTION_SERVICE = 4000
    STEP_ACTION_SESSION = 5000
    STEP_ACTION_SIMPLE = 6000

class ColumnName:
    ACTION = 0
    OBJECT = 1
    PARAMETER = 2

class Step(object):
    def __init__(self):
        self.type = StepType.STEP
        self.parent = None
        self.data = {} # attributes, name value paires
        self.children = []

    def load(self, node, parentStep):
        self.parent = parentStep

    def save(self):
        pass

    def row(self):
        pass

    def rowNumber(self, childStep):
        return self.children.index(childStep)

    def dataForColumn(self, column):
        pass

    def hasChildren(self):
        if len(self.children) > 0:
            return True
        else:
            return False

    def childCount(self):
        return len(self.children)

    def child(self, row):
        return self.children[row]

    def _getElementNameAndTextValue(self, theDic, node):
        """
        <haha>the text value</haha>  -> {'haha': 'the text value'}
        <haha></haha>  -> {'haha':'not available'}
        """
        text = ''.join([n.data for n in node.childNodes if n.nodeType == node.TEXT_NODE])
        if text == '':
            text = 'not available'
        theDic.update({node.tagName : text})

    def _getAttrNameValuePairs(self, node, attrNames):
        if node.nodeType != Node.ELEMENT_NODE:
            return {}

        return {attr : node.getAttribute(attr) for attr in attrNames}

class StepTestCase(Step):
    def __init__(self):
        super(StepTestCase, self).__init__()
        self.type = StepType.STEP_TESTCASE

    def load(self, node, parentStep):
        super(StepTestCase, self).load(node, parentStep)

        # get data for testcase step
        self.data.update(self._getAttrNameValuePairs(node, ['version', 'tcid', 'qcid']))

        generalNode = node.getElementsByTagName('general')[0];
        for n in generalNode.childNodes:
            if n.nodeType == Node.ELEMENT_NODE:
                self._getElementNameAndTextValue(self.data, n)

        #Functions
        functionNodes = node.getElementsByTagName('procedure')
        for childNode in functionNodes:
            if childNode.nodeType == Node.ELEMENT_NODE:
                step = StepFactory.createStep(childNode)
                self.children.append(step)
                step.load(childNode, self)

class StepFunction(Step):
    def __init__(self):
        super(StepFunction, self).__init__()
        self.type = StepType.STEP_FUNCTION

    def dataForColumn(self, column):
        super(StepFunction, self).dataForColumn(column)
        if column == ColumnName.ACTION:
            return 'function'
        elif column == ColumnName.OBJECT:
            return ''
        elif column == ColumnName.PARAMETER:
            return self.data['name']
        else:
            return None

    def load(self, node, parentStep):
        super(StepFunction, self).load(node, parentStep)

        self.data.update(self._getAttrNameValuePairs(node, ['desc', 'type', 'name']))

        # Arguments
        argElements = node.getElementsByTagName('arguments')[0].getElementsByTagName('arg')
        self.data['arguments'] = [self._getAttrNameValuePairs(argElment,
                                        ['desc', 'attribute', 'available', 'type', 'value', 'name'])
                                        for argElment in argElements]

        # Variable
        varElements = node.getElementsByTagName('variables')[0].getElementsByTagName('var')
        self.data['variables'] = [self._getAttrNameValuePairs(varElement,
                                    ['desc', 'type', 'value', 'name'])
                                    for varElement in varElements]

        # Steps
        stepsNode = node.getElementsByTagName('steps')[0]
        for childNode in stepsNode.childNodes:
            if childNode.nodeType == Node.ELEMENT_NODE:
                step = StepFactory.createStep(childNode)
                self.children.append(step)
                step.load(childNode, self)

class StepAction(Step):

    def dataForColumn(self, column):
        super(StepAction, self).dataForColumn(column)
        if column == ColumnName.ACTION:
            return self.data['action']
        elif column == ColumnName.OBJECT:
            return self.data['object']
        elif column == ColumnName.PARAMETER:
            return self.data['parameter']
        else:
            return None

    def load(self, node, parentStep):
        super(StepAction, self).load(node, parentStep)
        # <step action="open" uuid="{2339dfce-7024-43d2-a86d-be357b1ccb06}" object="tss" >
        self.data.update(self._getAttrNameValuePairs(node, ['action', 'uuid', 'object']))

        # <parameter>$ts_host -reuse gtss</parameter>
        parameterNode = node.getElementsByTagName('parameter')[0];
        self._getElementNameAndTextValue(self.data, parameterNode)

        # <response/>

        # <subSteps>
        subStepsNodes = node.getElementsByTagName('subSteps');
        if len(subStepsNodes) > 0:
            subStepsNode = subStepsNodes[0]

            for childNode in subStepsNode.childNodes:
                if childNode.nodeType == Node.ELEMENT_NODE:
                    step = StepFactory.createStep(childNode)
                    self.children.append(step)
                    step.load(childNode, self)


class StepActionService(StepAction):
    def load(self, node, parentStep):
        super(StepActionService, self).load(node, parentStep)

class StepActionSimple(StepAction):
    def load(self, node, parentStep):
        super(StepActionSimple, self).load(node, parentStep)

class StepActionSession(StepAction):
    def load(self, node, parentStep):
        super(StepActionSession, self).load(node, parentStep)

class StepFactory:
    @classmethod
    def createStep(cls, node):
        if node.nodeType != Node.ELEMENT_NODE:
            return None

        tagName = node.tagName
        if tagName == 'testCase':
            return StepTestCase()
        elif tagName == 'procedure':
            return StepFunction()
        elif tagName == 'step':
            o = node.getAttribute('object').strip()
            a = node.getAttribute('action')

            if len(o)> 0:
                #service or session
                if a in ['open', 'close', 'password', 'command', 'setPrompt']:
                    return StepActionSession()
                else:
                    return StepActionService()
            else:
                 return StepActionSimple()
        else:
            return None


class TestCase(object):
    '''
    classdocs
    '''
    def __init__(self, tcFileName):
        '''
        Constructor
        '''
        self.tcFileName = tcFileName
        self.rootStep = None

    def printout(self, node, prefix):
        if node.nodeType != Node.ELEMENT_NODE:
            return

        print(prefix + node.tagName)

        if node.hasChildNodes():
            prefix = prefix + '    '
            for child in node.childNodes:
                self.printout(child, prefix)


    def load(self):
        '''
        Load an XML TC to build a tree in memory
        '''

        tcString = self._readTestCase(self.tcFileName)
        doc = minidom.parseString(tcString)
        self.rootStep = StepTestCase()
        self.rootStep.load(doc.documentElement, None)

        # self.printout(doc.documentElement, '')

    def save(self):
        '''
        Dump the test case tree in memory into a XML TC file
        '''
        pass

    def _readTestCase(self, tcFileName):
        f = open(tcFileName)
        text = f.read()
        f.close()

        return cleanInvalidXmlChars(text)

def cleanInvalidXmlChars(dirtyXmlString):
    myre = re.compile('[\x3f\xa1\xa5\xa6\xe2\x80\x98\x99\x9c\x9d]')
    return myre.sub('', dirtyXmlString)

if __name__ == '__main__':
    tc = TestCase('D:\\Repository\\R_2_10_0\\doc\\examples\\service\\MS_LTE\\Attach.tc')
    tc.load()
    print('haha')
