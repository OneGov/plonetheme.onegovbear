from plone.app.theming.interfaces import IThemeSettings
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility


def installed(site):
    add_css_conditions(site)


def uninstalled(site):
    remove_css_conditions(site)
    uninstall_theme_settings()


def add_css_conditions(site):
    for resource in getToolByName(site, 'portal_css').getResources():
        if resource.getId() == 'members.css':
            # See cssregistry.xml
            continue

        resource.setExpression('not:request/HTTP_X_FTW_THEMING|nothing')


def remove_css_conditions(site):
    portal_css = getToolByName(site, 'portal_css')
    for resource in portal_css.getResources():
        if resource.getExpression() == (
                'not:request/HTTP_X_FTW_THEMING|nothing'):
            resource.setExpression('')


def uninstall_theme_settings():
    settings = getUtility(IRegistry).forInterface(IThemeSettings)
    registry = getUtility(IRegistry)

    if settings.currentTheme != 'plonetheme.onegovbear':
        return

    settings.currentTheme = None
    settings.enabled = False
    settings.doctype = ''
    settings.rules = None
    settings.absolutePrefix = None

    if 'pathbar_full_width' in settings.parameterExpressions:
        del settings.parameterExpressions['pathbar_full_width']

    field = registry.records['{}.parameterExpressions'.format(
        IThemeSettings.__identifier__)]
    if 'pathbar_full_width' in field._field.default:
        del field._field.default['pathbar_full_width']
