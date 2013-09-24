class Visitor(object):
    def visit(self, node):
        methodname = 'visit_' + type(node).__name__
        method = getattr(self, methodname, None)
        if method is None:
            method = self.generic_visit

        return method(node)

    def generic_visit(self, node):
        raise RuntimeError('No {} method'.format('visit_' + type(node).__name__))
