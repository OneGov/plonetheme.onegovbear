from Acquisition import aq_chain
from ftw.theming.interfaces import ISCSSResourceFactory
from ftw.theming.resource import SCSSResource
from plonetheme.onegovbear.browser.forms import VARIABLES_ANNOTATION_KEY
from plonetheme.onegovbear.interfaces import ICustomDesignVariablesSchema
from zope.annotation import IAnnotations
from zope.component import queryMultiAdapter
from zope.interface import implements
from zope.schema import getFields, getFieldNamesInOrder


class CustomDesignVariablesResourceFactory(object):
    implements(ISCSSResourceFactory)
    annotations_key = VARIABLES_ANNOTATION_KEY

    def __call__(self, context, request):
        self.context = context
        self.request = request
        return self.get_resource()

    def get_resource(self):
        source = self.get_source()
        return SCSSResource(VARIABLES_ANNOTATION_KEY, slot='variables',
                            source=source)

    def get_source(self):
        ancestor_variables = self.get_ancestor_variables()

        source = '\n'.join(
            '{0}: {1};'.format(name, value)
            for name, value in ancestor_variables
        )
        return source

    def get_ancestor_variables(self):
        for variables in map(self.get_scss_variables,
                             reversed(aq_chain(self.context))):
            for name, value in variables:
                if not value:
                    continue
                yield value['variable_name'], value['value']

    def get_scss_variables(self, obj):
        # import pdb; pdb.set_trace();
        # if not IAnnotations.providedBy(obj):
        #     return

        schema = queryMultiAdapter((obj, self.request),
                                   ICustomDesignVariablesSchema)
        if not schema:
            return

        annotations = IAnnotations(obj)
        variables = annotations.get(VARIABLES_ANNOTATION_KEY) or {}

        form_fields = getFields(schema)
        for field_name in getFieldNamesInOrder(schema):
            yield (form_fields[field_name].variable_name,
                   variables.get(field_name))

factory = CustomDesignVariablesResourceFactory()
