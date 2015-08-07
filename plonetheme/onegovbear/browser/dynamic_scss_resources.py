from Acquisition._Acquisition import aq_inner
from Acquisition._Acquisition import aq_parent
from Products.CMFPlone.interfaces import IPloneSiteRoot
from ftw.theming.interfaces import ISCSSResourceFactory
from ftw.theming.resource import SCSSResource
from plonetheme.onegovbear.browser.forms import ANNOTATION_KEY
from zope.annotation import IAnnotations
from zope.interface import provider


@provider(ISCSSResourceFactory)
def custom_scss_variables(context, request):

    parent_scss_variables = get_parent_scss_variables(context)
    context_scss_variables = get_scss_variables(context)

    combined_scss_variables = combine_scss_variables(parent_scss_variables,
                                                     context_scss_variables)

    source = ''
    if combined_scss_variables:
        source = '; '.join(
            ['{0}: {1}'.format(value['variable_name'], value['value'])
             for value in combined_scss_variables.itervalues()]
        ) + ';'

    return SCSSResource('plonetheme.onegovbear.custom.scss',
                        slot='variables',
                        source=source)


def get_scss_variables(context):
    annotations = IAnnotations(context)
    return annotations.get(ANNOTATION_KEY) or {}


def get_parent_scss_variables(context):
    if IPloneSiteRoot.providedBy(context):
        return {}
    parent = aq_parent(aq_inner(context))
    return get_scss_variables(parent)


def combine_scss_variables(parent_scss_variables, context_scss_variables):
    combined_scss_variables = parent_scss_variables.copy()
    combined_scss_variables.update(context_scss_variables)
    return combined_scss_variables
