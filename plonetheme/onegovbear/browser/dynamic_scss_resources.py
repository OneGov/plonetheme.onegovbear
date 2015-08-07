from Acquisition._Acquisition import aq_inner
from Acquisition._Acquisition import aq_parent
from Products.CMFPlone.interfaces import IPloneSiteRoot
from ftw.theming.interfaces import ISCSSResourceFactory
from ftw.theming.resource import SCSSResource
from plone.app.layout.navigation.interfaces import INavigationRoot
from plonetheme.onegovbear.browser.forms import ANNOTATION_KEY
from zope.annotation import IAnnotations
from zope.interface import implements


class CustomVariablesResourceFactory(object):
    implements(ISCSSResourceFactory)
    annotations_key = ANNOTATION_KEY

    def __call__(self, context, request):
        self.context = context
        self.request = request
        return self.get_resource()

    def get_resource(self):
        source = self.get_source()
        return SCSSResource(ANNOTATION_KEY, slot='variables', source=source)

    def get_source(self):
        ancestor_variables = self.get_ancestor_variables()

        variables = {}
        for d in ancestor_variables:
            variables.update(d)

        source = ''
        if variables:
            source = '; '.join(
                ['{0}: {1}'.format(value['variable_name'], value['value'])
                 for value in variables.itervalues()]
            ) + ';'
        return source

    def get_ancestor_variables(self):
        obj = self.context
        ancestor_variables = []
        while True:
            variables = self.get_scss_variables(obj)
            if variables:
                ancestor_variables.append(variables)
            if IPloneSiteRoot.providedBy(obj):
                break
            obj = aq_parent(aq_inner(obj))
        # Inverse the list so the top most variables come first.
        return reversed(ancestor_variables)

    def get_scss_variables(self, obj):
        if not INavigationRoot.providedBy(obj):
            return {}
        annotations = IAnnotations(obj)
        return annotations.get(ANNOTATION_KEY) or {}

factory = CustomVariablesResourceFactory()
