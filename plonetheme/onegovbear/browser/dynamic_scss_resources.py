from Acquisition._Acquisition import aq_inner
from Acquisition._Acquisition import aq_parent
from Products.CMFPlone.interfaces import IPloneSiteRoot
from ftw.theming.interfaces import ISCSSResourceFactory
from ftw.theming.resource import SCSSResource
from plone.app.layout.navigation.interfaces import INavigationRoot
from plonetheme.onegovbear.browser.forms import ANNOTATION_KEY
from zope.annotation import IAnnotations
from zope.interface import provider


@provider(ISCSSResourceFactory)
def custom_scss_variables(context, request):
    ancestor_variables = get_ancestor_variables(context)

    variables = {}
    for d in ancestor_variables:
        variables.update(d)

    source = ''
    if variables:
        source = '; '.join(
            ['{0}: {1}'.format(value['variable_name'], value['value'])
             for value in variables.itervalues()]
        ) + ';'

    return SCSSResource(ANNOTATION_KEY, slot='variables', source=source)


def get_ancestor_variables(context):
    ancestor_variables = []
    while True:
        variables = get_scss_variables(context)
        if variables:
            ancestor_variables.append(variables)
        if IPloneSiteRoot.providedBy(context):
            break
        context = aq_parent(aq_inner(context))
    # Inverse the list so the top most variables come first.
    return reversed(ancestor_variables)


def get_scss_variables(context):
    if not INavigationRoot.providedBy(context):
        return {}
    annotations = IAnnotations(context)
    return annotations.get(ANNOTATION_KEY) or {}
