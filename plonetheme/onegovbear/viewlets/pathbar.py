from plone.app.layout.viewlets import common
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class PathBarViewlet(common.PathBarViewlet):
    pathbar = ViewPageTemplateFile('pathbar.pt')

    def index(self):
        return self.pathbar()
