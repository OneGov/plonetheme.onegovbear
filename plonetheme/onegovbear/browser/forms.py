from persistent.mapping import PersistentMapping
from plone.directives import form
from plone.z3cform.layout import wrap_form
from plonetheme.onegovbear import _
from plonetheme.onegovbear.browser.fields import Variable
from zope.annotation import IAnnotations
from zope.interface import implements

ANNOTATION_KEY = 'plonetheme.onegovebear.custom_scss_variables'


class IVariablesSchema(form.Schema):
    primary_color = Variable('$primary-color')
    secondary_color = Variable('$secondary-color')
    globalnav_bg_color = Variable('$globalnav-bg-color')
    globalnav_bg_color_hover = Variable('$globalnav-bg-color-hover')
    globalnav_link_color = Variable('$globalnav-link-color')
    globalnav_link_color_hover = Variable('$globalnav-link-color-hover')
    globalnav_separator_color = Variable('$globalnav-separator-color')
    button_standalone_color = Variable('$button-standalone-color')
    button_context_color = Variable('$button-context-color')
    button_destructive_color = Variable('$button-destructive-color')
    button_success_color = Variable('$button-success-color')
    button_warning_color = Variable('$button-warning-color')
    button_danger_color = Variable('$button-danger-color')
    button_disabled_color = Variable('$button-disabled-color')
    button_text_light_color = Variable('$button-text-light-color')
    button_text_dark_color = Variable('$button-text-dark-color')
    footer_background_color = Variable('$footer-background-color')
    footer_font_color = Variable('$footer-font-color')
    footer_link_color = Variable('$footer-link-color')
    footer_link_color_hover = Variable('$footer-link-color-hover')
    font_family_base = Variable('$font-family-base')
    line_height_base = Variable('$line-height-base')
    font_size_base = Variable('$font-size-base')
    font_size_h1 = Variable('$font-size-h1')
    font_size_h2 = Variable('$font-size-h2')
    font_size_h3 = Variable('$font-size-h3')
    page_bg_color = Variable('$page-bg-color')
    gray_base = Variable('$gray-base')
    gray_darker = Variable('$gray-darker')
    gray_dark = Variable('$gray-dark')
    gray = Variable('$gray')
    gray_light = Variable('$gray-light')
    gray_lighter = Variable('$gray-lighter')


class VariablesConfig(object):
    """
    This proxy object saves the name of the form field, its value and
    the SCSS variable name. We need the SCSS variable name later when
    returning the variables in the dynamic SCSS resource factory.
    Example:

        {'service_nav_link_color': {
            'value': u'green', 'variable_name':
            '$service-nav-link-color'}
        }
    """
    implements(IVariablesSchema)
    _protected_names = ['storage', 'fields']

    def __init__(self, storage, fields):
        self.storage = storage
        self.fields = fields

    def __getattr__(self, name):
        if name in self._protected_names:
            return object.__getattr__(self, name)
        value = self.storage.get(name)
        return value.get('value')

    def __setattr__(self, name, value):
        if name in self._protected_names:
            return object.__setattr__(self, name, value)
        if value:
            self.storage[name] = {
                'value': value,
                'variable_name': self.fields._data[name].field.variable_name
            }
        elif name in self.storage:
            del self.storage[name]


class VariablesForm(form.SchemaEditForm):
    """
    This form is used to customize the SCSS variables. Subclasses must
    override `annotation_key` and `config` and implement their own config
    class with a custom schema.
    """
    label = _(u'variables_form_label', default=u'Custom SCSS variables')
    description = _(u'variables_form_description',
                    default=u'The values entered in this form will override '
                            u'the SCSS variables defined in the theme for the '
                            u'INavigationRoot (e.g. Plone Site and Subsites).')
    schema = IVariablesSchema
    ignoreContext = False
    annotation_key = ANNOTATION_KEY
    config = VariablesConfig

    def getContent(self):
        annotations = IAnnotations(self.context)
        if self.annotation_key not in annotations:
            annotations[self.annotation_key] = PersistentMapping()

        # In case a field is removed from the schema which previously
        # has been used to override a SCSS variable its value becomes stale.
        # The stale value needs to be removed from the annotations
        # since it cannot be removed in the form due to the missing form
        # field. This is done by rebuilding the value stored in the
        # annotations.
        cleaned = {}
        for key in self.fields.keys():
            if key in annotations[self.annotation_key].keys():
                cleaned[key] = annotations[self.annotation_key][key]
        annotations[self.annotation_key] = cleaned

        return self.config(annotations[self.annotation_key], self.fields)

WrappedVariablesForm = wrap_form(VariablesForm)
