from testcase import testcase
from testcase import visitor

class Tc2Tet(visitor.Visitor):
    tcTemplate = """Testcase General Information
TC_ID {tcid}
QC_ID {qcid}
Title {title}
Author {author}
Created {created}
Purpose {purpose}
Usage {usage}
"""
    functionTemplate = """function::{name}
  {name}:description
{description}

  {name}:arguments
{arguments}

  {name}:variables
{variables}

  {name}:steps"""

    def __init__(self):
        self.tcFileName = ''
        self.level = 0
        self.tet = []

    def _getIndent(self):
        return  '    ' + '  ' * self.level

    def transformFromTestCase(self, tc):
        self.tcFileName = tc.tcFileName

        self.visit(tc.rootStep)

        return '\n'.join(self.tet)

    def transform(self, fileLocation):
        self.tcFileName = fileLocation
        tc = testcase.TestCase(fileLocation)
        tc.load()

        self.visit(tc.rootStep)

        return '\n'.join(self.tet)

    def visit_StepTestCase(self, node):
        self.tet.append(
            self.tcTemplate.format(tcid=node.data['tcid'],
                qcid=node.data['qcid'],
                title=node.data['title'],
                author=node.data['author'],
                created=node.data['created'],
                purpose=node.data['purpose'],
                usage=node.data['usage'])
        )

        for eachFunction in node.children:
            self.visit(eachFunction)

    def visit_StepFunction(self, node):
        arguments = ['{indent}{type} {name}'.format(indent = self._getIndent(), type = arg['type'], name = arg['name'])
                      for arg in node.data['arguments']]

        variables = ['{indent}{type} {name}'.format(indent = self._getIndent(), type = var['type'], name = var['name'])
                      for var in node.data['variables']]

        self.tet.append(
            self.functionTemplate.format(name = node.data['name'],
                description = self._getIndent() + node.data['desc'],
                arguments = '\n'.join(arguments),
                variables = '\n'.join(variables))
        )

        for eachStep in node.children:
            self.visit(eachStep)

    def visit_StepActionService(self, node):
        self.tet.append('{indent}{object}.{action} {parameter}'.format(
            indent = self._getIndent(),
            object = node.data['object'],
            action = node.data['action'],
            parameter = node.data['parameter']))

        self.level += 1
        for eachSubStep in node.children:
            self.visit(eachSubStep)
        self.level -= 1

    def visit_StepActionSimple(self, node):
        self.tet.append('{indent}{action} {parameter}'.format(
            indent = self._getIndent(),
            action = node.data['action'],
            parameter = node.data['parameter']))

        self.level += 1
        for eachSubStep in node.children:
            self.visit(eachSubStep)
        self.level -= 1

    def visit_StepActionSession(self, node):
        self.tet.append('{indent}{object}.{action} {parameter}'.format(
            indent = self._getIndent(),
            object = node.data['object'],
            action = node.data['action'],
            parameter = node.data['parameter']))

        self.level += 1
        for eachSubStep in node.children:
            self.visit(eachSubStep)
        self.level -= 1

if __name__ == '__main__':
    t = Tc2Tet()
    print(t.transform('C:\\Users\\zhzhong\\.EasyTest\\2.7.1Free\\workspace\\tc\\language\\action\\assertEqual\\testAction_assertEqual_UsingVariableForRegExpString.tc'))
