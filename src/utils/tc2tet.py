from PySide import QtCore
from PySide import QtGui
import xml.dom.minidom

class Tc2Tet(object):
    def __init__(self):
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

    def transform(self, fileLocation):        
        dom = xml.dom.minidom.parse(fileLocation)
        testCaseElement = dom.documentElement
        tc = {}
        tc['tcid'] = testCaseElement.getAttribute('tcid')
        tc['qcid'] = testCaseElement.getAttribute('qcid')

        generalElement = testCaseElement.getElementsByTagName('general')[0]
        tc['author'] = generalElement.getElementsByTagName('author')[0].childNodes[0].nodeValue
        tc['created'] = generalElement.getElementsByTagName('created')[0].childNodes[0].nodeValue
        tc['purpose'] = generalElement.getElementsByTagName('purpose')[0].childNodes[0].nodeValue
        tc['usage'] = generalElement.getElementsByTagName('usage')[0].childNodes[0].nodeValue
        tc['title'] = generalElement.getElementsByTagName('title')[0].childNodes[0].nodeValue
        tc['functions'] = ""

        oneFunction = {'name':""}

        functionElements = testCaseElement.getElementsByTagName('procedure')
        for functionElement in functionElements:
            oneFunction['name'] = functionElement.getAttribute('name')
            oneFunction['description'] = functionElement.getAttribute('desc')

            argumentsElement = functionElement.getElementsByTagName('arguments')[0].getElementsByTagName('arg')
            args = []
            for argElement in argumentsElement:
                args.append('{type} {name}\n'.format(type = argElement.getAttribute('type'), name = argElement.getAttribute('name')))
            oneFunction['arguments'] = '\n'.join(args)

            variablesElement = functionElement.getElementsByTagName('variables')[0].getElementsByTagName('var')
            vars = []
            for varElement in variablesElement:
                vars.append('{type} {name}\n'.format(type = varElement.getAttribute('type'), name = varElement.getAttribute('name')))
            oneFunction['variables'] = '\n'.join(vars)

            stepsElement = functionElement.getElementsByTagName('steps')

            oneFunction['steps'] = ""


            tc['functions'] += self.functionTemplate.format(**oneFunction)

        return self.tcTemplate.format(**tc)

if __name__ == '__main__':
    t = Tc2Tet()
    print(t.transform('if_else.tc'))
    
