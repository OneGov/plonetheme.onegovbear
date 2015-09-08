from plone import api
from plone.app.layout.viewlets import common
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class OneGovBearSkipLinksViewlet(common.SkipLinksViewlet):
    index = ViewPageTemplateFile('accesskeys.pt')

    def update(self):
        super(OneGovBearSkipLinksViewlet, self).update()
        self.nav_root_url = api.portal.get_navigation_root(
            self.context).absolute_url()
