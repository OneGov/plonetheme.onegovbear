from ftw.testbrowser import browsing
from plonetheme.onegovbear.browser.forms import ANNOTATION_KEY
from plonetheme.onegovbear.tests import FunctionalTestCase
from zope.annotation import IAnnotations


class TestCustomSCSSVariables(FunctionalTestCase):

    def setUp(self):
        super(TestCustomSCSSVariables, self).setUp()
        self.grant('Manager')

    @browsing
    def test_values_in_annotations(self, browser):
        browser.login().visit(self.portal, view='customize-design')
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
