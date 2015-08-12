from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.statusmessages.interfaces import IStatusMessage
from persistent.mapping import PersistentMapping
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.directives import form
from plone.z3cform.layout import wrap_form
from plonetheme.onegovbear import _
from plonetheme.onegovbear.interfaces import ICustomDesignVariablesSchema
from z3c.form import button
from zope.annotation import IAnnotations
from zope.component import adapter, getMultiAdapter
from zope.i18n import translate
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.interface import Interface
from zope.schema import TextLine
from zope.schema._compat import u
import time

VARIABLES_ANNOTATION_KEY = 'plonetheme.onegovebear.custom_scss_variables'
TIMESTAMP_ANNOTATION_KEY = VARIABLES_ANNOTATION_KEY + '.last_update_timestamp'


class Variable(TextLine):
    def __init__(self, variable_name=None, **kw):
        self.variable_name = variable_name

        if not variable_name:
            self.variable_name = '$' + self.__name__

        if 'title' not in kw:
            kw['title'] = u(self.variable_name)

        if 'required' not in kw:
            kw['required'] = False

        super(Variable, self).__init__(**kw)


class IDefaultDesignVariablesSchema(form.Schema):
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


@adapter(INavigationRoot, Interface)
@implementer(ICustomDesignVariablesSchema)
def get_default_design_variables_schema(context, request):
    return IDefaultDesignVariablesSchema


class DesignVariablesConfig(object):
    """
    This proxy object saves the name of the form field, its value and
    the SCSS variable name. We need the SCSS variable name later when
    returning the variables in the dynamic SCSS resource factory.
    Example:

        {'service_nav_link_color': {
            'value': u'green',
            'variable_name': '$service-nav-link-color'}
        }
    """
    _protected_names = ['storage', 'fields', '__provides__']

    def __init__(self, storage, fields):
        self.storage = storage
        self.fields = fields

    def __getattr__(self, name):
        if name in self._protected_names:
            return self.__dict__.get(name)
        value = self.storage.get(name)
        return value.get('value')

    def __setattr__(self, name, value):
        if name in self._protected_names:
            self.__dict__[name] = value
            return
        if value:
            self.storage[name] = {
                'value': value,
                'variable_name': self.fields._data[name].field.variable_name
            }
        elif name in self.storage:
            del self.storage[name]


class DesignVariablesForm(form.SchemaEditForm):
    label = _(u'variables_form_label',
              default=u'Custom design variables (SCSS)')
    ignoreContext = False

    @property
    def description(self):
        description = translate(
            _(u'variables_form_description',
              default=u'This form can be used to customize a selection of the '
                      u'design variable defined in this theme.'),
            context=self.request)

        if not IPloneSiteRoot.providedBy(self.context):
            description += '<br />' + translate(
                _(u'variables_form_description_inheritance',
                  default=u'Variables will be inherited from the ancestors.'),
                context=self.request)
        return description

    @property
    def schema(self):
        return getMultiAdapter((self.context, self.request),
                               ICustomDesignVariablesSchema)

    def getContent(self):
        annotations = IAnnotations(self.context)
        if VARIABLES_ANNOTATION_KEY not in annotations:
            annotations[VARIABLES_ANNOTATION_KEY] = PersistentMapping()

        config = DesignVariablesConfig(annotations[VARIABLES_ANNOTATION_KEY],
                                       self.fields)
        alsoProvides(config, self.schema)

        return config

    @button.buttonAndHandler(_(u'Save'), name='save')
    def handleApply(self, action):
        """
        Based on `plone.directives.form.form.EditForm` but with a customized
        redirect url.
        """
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.applyChanges(data)

        annotations = IAnnotations(self.context)
        annotations[TIMESTAMP_ANNOTATION_KEY] = time.time()

        IStatusMessage(self.request).addStatusMessage(_(u'Changes saved'))
        self.request.response.redirect(self.redirect_url)

    @button.buttonAndHandler(_(u'Cancel'), name='cancel')
    def handleCancel(self, action):
        """
        Based on `plone.directives.form.form.EditForm` but with a customized
        redirect url.
        """
        IStatusMessage(self.request).addStatusMessage(_(u'Edit cancelled'))
        self.request.response.redirect(self.redirect_url)

    @property
    def redirect_url(self):
        return self.context.absolute_url() + '/@@customize-design'

    def update(self):
        super(DesignVariablesForm, self).update()
        self.request.set('disable_border', 1)

WrappedDesignVariablesForm = wrap_form(DesignVariablesForm)
