from PySide import QtCore
from PySide import QtGui
import xml.dom.minidom

class Tc2Tet(object):
    def __init__(self):
        self.indent = '  ' # 2 spaces indent
        self.leadingSpace = '    ' # 4 spaces
        self.tcTemplate = """Testcase General Information
TC_ID {tcid}
QC_ID {qcid}
Title {title}
Author {author}
Created {created}
Purpose {purpose}

Usage {usage}

{functions}"""
        self.functionTemplate = """function::{name}
  {name}:description 
{description}    
  {name}:arguments
{arguments}
  {name}:variables
{variables}
  {name}:steps
{steps}"""

    def transformStep(self, stepElement, indent):
        objectValue = stepElement.getAttribute('object')
        actionValue = stepElement.getAttribute('action')

        parameterValue = ''
        parameterElement = self.__getMyChildByTagName(stepElement, 'parameter')
        if len(parameterElement.childNodes) > 0:
            parameterValue = parameterElement.firstChild.data        
        
        transformedStepList = []

        if objectValue == ' ':
            transformedStepList.append('{0}{1} {2}'.format(indent, actionValue, parameterValue))
        else:
            transformedStepList.append('{0}{1}.{2} {3}'.format(indent, objectValue, actionValue, parameterValue))

        subStepsElenents = self.__getMyChildrenByTagName(stepElement, 'subSteps')
        if len(subStepsElenents) > 0:
            for e in self.__getMyChildrenByTagName(subStepsElenents[0], 'step'):
                transformedStepList.append(self.transformStep(e, indent + self.indent))

        return '\n'.join(transformedStepList)

    def __getMyChildrenByTagName(self, element, tagName):
        return [node for node in element.childNodes if node.nodeType==node.ELEMENT_NODE and node.tagName == tagName]        

    def __getMyChildByTagName(self, element, tagName):
        for node in element.childNodes:
            if node.nodeType==node.ELEMENT_NODE and node.tagName == tagName:
                return node

        return xml.dom.minidom.Element

    def transform(self, fileLocation):        
        dom = xml.dom.minidom.parse(fileLocation)
        testCaseElement = dom.documentElement
        tc = {}
        tc['tcid'] = testCaseElement.getAttribute('tcid')
        tc['qcid'] = testCaseElement.getAttribute('qcid')

        generalElement = self.__getMyChildByTagName(testCaseElement, 'general')
        tc['author'] = self.__getMyChildByTagName(generalElement, 'author').firstChild.data
        tc['created'] = self.__getMyChildByTagName(generalElement, 'created').firstChild.data
        tc['purpose'] = self.__getMyChildByTagName(generalElement, 'purpose').firstChild.data
        tc['usage'] = self.__getMyChildByTagName(generalElement, 'usage').firstChild.data
        tc['title'] = self.__getMyChildByTagName(generalElement, 'title').firstChild.data
        tc['functions'] = ""

        oneFunction = {'name':""}

        functionElements = testCaseElement.getElementsByTagName('procedure')
        for functionElement in functionElements:
            oneFunction['name'] = functionElement.getAttribute('name')
            oneFunction['description'] = self.indent + functionElement.getAttribute('desc')

            argumentsElement = functionElement.getElementsByTagName('arguments')[0].getElementsByTagName('arg')
            args = []
            for argElement in argumentsElement:
                args.append('{indent}{type} {name}'.format(indent = self.leadingSpace, type = argElement.getAttribute('type'), name = argElement.getAttribute('name')))
            oneFunction['arguments'] = '\n'.join(args)

            variablesElement = functionElement.getElementsByTagName('variables')[0].getElementsByTagName('var')
            vars = []
            for varElement in variablesElement:
                vars.append('{indent}{type} {name}'.format(indent = self.leadingSpace, type = varElement.getAttribute('type'), name = varElement.getAttribute('name')))
            oneFunction['variables'] = '\n'.join(vars)
            
            transformedStepList = []
            stepsElement = self.__getMyChildByTagName(functionElement, 'steps')
            stepElements = self.__getMyChildrenByTagName(stepsElement, 'step')
            for stepElement in stepElements:
                transformedStepList.append(self.transformStep(stepElement, self.leadingSpace))

            oneFunction['steps'] = '\n'.join(transformedStepList)
            
        tc['functions'] += self.functionTemplate.format(**oneFunction)

        return self.tcTemplate.format(**tc)

if __name__ == '__main__':
    t = Tc2Tet()
    print(t.transform('if_else.tc'))
    # with open('if_else.tc') as file:
    #     content = file.read()
    #     print(t.transform(content))
    
