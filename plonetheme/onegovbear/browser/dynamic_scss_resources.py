from ftw.theming.interfaces import ISCSSResourceFactory
from ftw.theming.resource import SCSSResource
from plonetheme.onegovbear.browser.forms import ANNOTATION_KEY
from zope.annotation import IAnnotations
from zope.interface import provider


@provider(ISCSSResourceFactory)
def custom_scss_variables(context, request):

    annotations = IAnnotations(context)
    scss_variables = annotations.get(ANNOTATION_KEY)

    source = ''
    if scss_variables:
        source = '; '.join(
            ['{0}: {1}'.format(value['variable_name'], value['value'])
             for value in scss_variables.itervalues()]
        ) + ';'

    return SCSSResource('plonetheme.onegovbear.custom.scss',
                        slot='addon',
                        source=source)
