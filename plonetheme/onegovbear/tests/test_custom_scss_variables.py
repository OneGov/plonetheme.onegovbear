from ftw.testbrowser import browsing
from ftw.builder import Builder
from ftw.builder import create
from plonetheme.onegovbear.browser.dynamic_scss_resources import \
    custom_scss_variables
from plonetheme.onegovbear.browser.forms import ANNOTATION_KEY
from plonetheme.onegovbear.tests import FunctionalTestCase
from zope.annotation import IAnnotations


class TestCustomSCSSVariables(FunctionalTestCase):

    def setUp(self):
        super(TestCustomSCSSVariables, self).setUp()
        self.grant('Manager')

    @browsing
    def test_values_in_annotations(self, browser):
        browser.login()
        browser.visit(self.portal, view='customize-design')
        browser.fill({
            '$primary-color': '#FF00FF',
            '$secondary-color': 'red',
        }).save()

        annotations = IAnnotations(self.portal)
        self.assertEqual(
            {'primary_color': {'value': u'#FF00FF',
                               'variable_name': '$primary-color'},
             'secondary_color': {'value': u'red',
                                 'variable_name': '$secondary-color'}},
            annotations[ANNOTATION_KEY])

    @browsing
    def test_value_inheritance(self, browser):
        browser.login()
        browser.visit(self.portal, view='customize-design')
        browser.fill({
            '$primary-color': 'blue',
            '$secondary-color': 'red',
        }).save()

        page = create(Builder('subsite').titled(u'My Subsite'))
        browser.visit(page, view='customize-design')
        browser.fill({
            '$secondary-color': 'green',
        }).save()

        scss_resource = custom_scss_variables(page, self.request)
        self.assertEqual(
            '$primary-color: blue; $secondary-color: green;',
            scss_resource.source
        )

