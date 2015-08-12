from ftw.builder import Builder
from ftw.builder import create
from ftw.testbrowser import browsing
from plone.app.layout.navigation.interfaces import INavigationRoot
from plonetheme.onegovbear.browser.dynamic_scss_resources import custom_design_variables_resource_factory
from plonetheme.onegovbear.browser.forms import VARIABLES_ANNOTATION_KEY
from plonetheme.onegovbear.tests import FunctionalTestCase
from zope.annotation import IAnnotations
import transaction


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
            annotations[VARIABLES_ANNOTATION_KEY])

    @browsing
    def test_value_inheritance(self, browser):
        browser.login()
        browser.visit(self.portal, view='customize-design')
        browser.fill({
            '$primary-color': 'blue',
            '$secondary-color': 'red',
            '$globalnav-bg-color': 'fuchsia',
        }).save()

        page = create(Builder('folder').titled(u'My Subsite').providing(INavigationRoot))
        browser.visit(page, view='customize-design')
        browser.fill({
            '$secondary-color': 'green',
        }).save()

        scss_resource = custom_design_variables_resource_factory(
            page, self.request)
        self.assertEqual(
            '$primary-color: blue;\n$secondary-color: red;\n'
            '$globalnav-bg-color: fuchsia;\n$secondary-color: green;',
            scss_resource.get_source(page, self.request)
        )

        page2 = create(Builder('folder').titled(u'My Subsite').within(page)
                       .providing(INavigationRoot))
        browser.visit(page2, view='customize-design')
        browser.fill({
            '$primary-color': 'yellow',
        }).save()

        scss_resource = custom_design_variables_resource_factory(
            page2, self.request)
        self.assertEqual(
            '$primary-color: blue;\n$secondary-color: red;\n'
            '$globalnav-bg-color: fuchsia;\n$secondary-color: green;\n'
            '$primary-color: yellow;',
            scss_resource.get_source(page2, self.request)
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

        scss_resource = custom_design_variables_resource_factory(
            self.portal, self.request)
        self.assertEqual(
            '$primary-color: blue;\n$secondary-color: red;',
            scss_resource.get_source(self.portal, self.request)
        )

        # Now empty a value and make sure its no longer there.
        browser.visit(self.portal, view='customize-design')
        browser.fill({
            '$primary-color': 'blue',
            '$secondary-color': '',
        }).save()

        scss_resource = custom_design_variables_resource_factory(
            self.portal, self.request)
        self.assertEqual(
            '$primary-color: blue;',
            scss_resource.get_source(self.portal, self.request)
        )

    @browsing
    def test_user_action(self, browser):
        action_link_label = 'Customize design'
        action_link_url = '@@customize-design'

        # Make sure the manager
        browser.login().visit(self.portal)
        self.assertEqual(
            action_link_url,
            browser.find(action_link_label).attrib['href']
        )

        # Make sure the action is not available for users
        # without the permission to configure the contact form.
        member = create(Builder('user')
                        .named('Hugo', 'Boss')
                        .with_roles('Member'))
        browser.login(member).visit(self.portal)
        self.assertIsNone(browser.find(action_link_label))

        # Give the user the permission to configure the contact form and
        # make sure the user can see the action.
        permissions = 'plonetheme.onegovbear: Customize Design Variables'
        self.portal.manage_permission(permissions, roles=['Member'],
                                      acquire=False)
        transaction.commit()
        browser.visit(self.portal)
        self.assertEqual(
            action_link_url,
            browser.find(action_link_label).attrib['href']
        )
