from ftw.testbrowser import browsing
from ftw.builder import Builder
from ftw.builder import create
from plonetheme.onegovbear.browser.dynamic_scss_resources import factory
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
            '$globalnav-bg-color': 'fuchsia',
        }).save()

        page = create(Builder('subsite').titled(u'My Subsite'))
        browser.visit(page, view='customize-design')
        browser.fill({
            '$secondary-color': 'green',
        }).save()

        scss_resource = factory(page, self.request)
        self.assertEqual(
            '$primary-color: blue; $globalnav-bg-color: fuchsia; '
            '$secondary-color: green;',
            scss_resource.source
        )

        page2 = create(Builder('subsite').titled(u'My Subsite').within(page))
        browser.visit(page2, view='customize-design')
        browser.fill({
            '$primary-color': 'yellow',
        }).save()

        scss_resource = factory(page2, self.request)
        self.assertEqual(
            '$primary-color: yellow; $globalnav-bg-color: fuchsia; '
            '$secondary-color: green;',
            scss_resource.source
        )

    @browsing
    def test_emptying_values(self, browser):
        """
        This test makes sure that when a custom variable is emptied it
        no longer is present in the storage.
        """
        browser.login()
        browser.visit(self.portal, view='customize-design')
        browser.fill({
            '$primary-color': 'blue',
            '$secondary-color': 'red',
        }).save()

        scss_resource = factory(self.portal, self.request)
        self.assertEqual(
            '$primary-color: blue; $secondary-color: red;',
            scss_resource.source
        )

        # Now empty a value and make sure its no longer there.
        browser.visit(self.portal, view='customize-design')
        browser.fill({
            '$primary-color': 'blue',
            '$secondary-color': '',
        }).save()

        scss_resource = factory(self.portal, self.request)
        self.assertEqual(
            '$primary-color: blue;',
            scss_resource.source
        )
