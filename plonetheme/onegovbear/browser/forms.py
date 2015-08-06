from persistent.mapping import PersistentMapping
from plone.directives import form
from plone.z3cform.layout import wrap_form
from plonetheme.onegovbear import _
from plonetheme.onegovbear.browser.fields import Variable
from zope.annotation import IAnnotations
from zope.interface import implements

ANNOTATION_KEY = 'plonetheme.onegovebear.custom_scss_variables'


class IVariablesSchema(form.Schema):
    primary_color = Variable(
        variable_name='$primary-color')
    secondary_color = Variable(
        variable_name='$secondary-color')
    globalnav_bg_color = Variable(
        variable_name='$globalnav-bg-color')
    globalnav_bg_color_hover = Variable(
        variable_name='$globalnav-bg-color-hover')
    globalnav_link_color = Variable(
        variable_name='$globalnav-link-color')
    globalnav_link_color_hover = Variable(
        variable_name='$globalnav-link-color-hover')
    globalnav_separator_color = Variable(
        variable_name='$globalnav-separator-color')
    button_standalone_color = Variable(
        variable_name='$button-standalone-color')
    button_context_color = Variable(
        variable_name='$button-context-color')
    button_destructive_color = Variable(
        variable_name='$button-destructive-color')
    button_success_color = Variable(
        variable_name='$button-success-color')
    button_warning_color = Variable(
        variable_name='$button-warning-color')
    button_danger_color = Variable(
        variable_name='$button-danger-color')
    button_disabled_color = Variable(
        variable_name='$button-disabled-color')
    button_text_light_color = Variable(
        variable_name='$button-text-light-color')
    button_text_dark_color = Variable(
        variable_name='$button-text-dark-color')
    footer_background_color = Variable(
        variable_name='$footer-background-color')
    footer_font_color = Variable(
        variable_name='$footer-font-color')
    footer_link_color = Variable(
        variable_name='$footer-link-color')
    footer_link_color_hover = Variable(
        variable_name='$footer-link-color-hover')
    font_family_base = Variable(
        variable_name='$font-family-base')
    line_height_base = Variable(
        variable_name='$line-height-base')
    font_size_base = Variable(
        variable_name='$font-size-base')
    font_size_h1 = Variable(
        variable_name='$font-size-h1')
    font_size_h2 = Variable(
        variable_name='$font-size-h2')
    font_size_h3 = Variable(
        variable_name='$font-size-h3')
    page_bg_color = Variable(
        variable_name='$page-bg-color')
    gray_base = Variable(
        variable_name='$gray-base')
    gray_darker = Variable(
        variable_name='$gray-darker')
    gray_dark = Variable(
        variable_name='$gray-dark')
    gray = Variable(
        variable_name='$gray')
    gray_light = Variable(
        variable_name='$gray-light')
    gray_lighter = Variable(
        variable_name='$gray-lighter')


class VariablesConfig(object):
    implements(IVariablesSchema)

    def __init__(self, storage):
        self.storage = storage

    def __getattr__(self, name):
        if name == 'storage':
            return object.__getattr__(self, name)
        value = self.storage.get(name)
        return value

    def __setattr__(self, name, value):
        if name == 'storage':
            return object.__setattr__(self, name, value)
        self.storage[name] = value


class VariablesForm(form.SchemaEditForm):
    label = _(u'variables_form_label', default=u'Custom SCSS variables')
    description = _(u'variables_form_description',
                    default=u'The values entered in this form will override '
                            u'the SCSS variables defined in the theme for the '
                            u'INavigationRoot (e.g. Plone Site and Subsites.)')
    schema = IVariablesSchema
    ignoreContext = False

    def getContent(self):
        annotations = IAnnotations(self.context)
        if ANNOTATION_KEY not in annotations:
            annotations[ANNOTATION_KEY] = PersistentMapping()
        return VariablesConfig(annotations[ANNOTATION_KEY])

VariablesForm = wrap_form(VariablesForm)
