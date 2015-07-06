from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common


class PathBarViewlet(common.PathBarViewlet):
    pathbar = ViewPageTemplateFile('pathbar.pt')

    def index(self):
        return self.pathbar()
