from ftw.theming.interfaces import ISCSSResourceFactory
from ftw.theming.resource import SCSSResource
from plonetheme.onegovbear.browser.forms import ANNOTATION_KEY
from zope.annotation import IAnnotations
from zope.interface import provider


@provider(ISCSSResourceFactory)
def custom_scss_variables(context, request):

    annotations = IAnnotations(context)
    values = annotations[ANNOTATION_KEY]

    source = '; '.join(
        '${0}: {1}'.format(key, value) for key, value in values.iteritems()
    ) + ';'

    return SCSSResource('plonetheme.onegovbear.custom.scss',
                        slot='addon',
                        source=source)
