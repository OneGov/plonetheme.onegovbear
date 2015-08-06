from zope.schema._bootstrapfields import TextLine
from zope.schema._compat import u


class Variable(TextLine):
    def __init__(self, variable_name, **kw):
        self.variable_name = variable_name

        if 'title' not in kw:
            kw['title'] = u(self.variable_name)

        if 'required' not in kw:
            kw['required'] = False

        super(Variable, self).__init__(**kw)
