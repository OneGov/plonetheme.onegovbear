from Acquisition import aq_chain
from ftw.theming.interfaces import ISCSSResourceFactory
from ftw.theming.resource import DynamicSCSSResource
from plonetheme.onegovbear.browser.forms import TIMESTAMP_ANNOTATION_KEY
from plonetheme.onegovbear.browser.forms import VARIABLES_ANNOTATION_KEY
from plonetheme.onegovbear.interfaces import ICustomDesignVariablesSchema
from zope.annotation import IAnnotations
from zope.component import queryMultiAdapter
from zope.interface import provider
from zope.schema import getFields, getFieldNamesInOrder


class CustomDesignVariablesSCSSResource(DynamicSCSSResource):

    def get_source(self, context, request):
        ancestor_variables = self._get_ancestor_variables(context)

        source = '\n'.join(
            '{0}: {1};'.format(name, value)
            for name, value in ancestor_variables
        )
        return source

    def get_cachekey(self, context, request):
        timestamps = [self._get_timestamp(ancestor) for ancestor
                      in self._get_ancestors(context)]
        timestamps = filter(None, timestamps)
        timestamps = map(str, timestamps)
        return '-'.join(timestamps)

    def _get_ancestors(self, obj):
        return reversed(aq_chain(obj))

    def _get_ancestor_variables(self, obj):
        for variables in map(self._get_scss_variables,
                             self._get_ancestors(obj)):
            for name, value in variables:
                if not value:
                    continue
                yield value['variable_name'], value['value']

    def _get_scss_variables(self, obj):
        schema = queryMultiAdapter((obj, obj.REQUEST),
                                   ICustomDesignVariablesSchema)
        if not schema:
            return

        annotations = IAnnotations(obj, None)
        if not annotations:
            return
        variables = annotations.get(VARIABLES_ANNOTATION_KEY) or {}

        form_fields = getFields(schema)
        for field_name in getFieldNamesInOrder(schema):
            yield (form_fields[field_name].variable_name,
                   variables.get(field_name))

    def _get_timestamp(self, obj):
        annotations = IAnnotations(obj, None)
        if not annotations:
            return None
        return annotations.get(TIMESTAMP_ANNOTATION_KEY, None)


@provider(ISCSSResourceFactory)
def custom_design_variables_resource_factory(context, request):
    return CustomDesignVariablesSCSSResource(
        'plonetheme.onegovbear.custom_design_variables.scss',
        slot='variables',
        before='ftw.theming:portal_url',
    )
