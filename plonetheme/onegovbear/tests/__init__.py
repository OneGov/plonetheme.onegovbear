from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plonetheme.onegovbear.testing import THEME_FUNCTIONAL
from unittest2 import TestCase
import transaction


class FunctionalTestCase(TestCase):
    layer = THEME_FUNCTIONAL

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def grant(self, *roles):
        setRoles(self.portal, TEST_USER_ID, roles)
        transaction.commit()
