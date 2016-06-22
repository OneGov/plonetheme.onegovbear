from ftw.subsite.interfaces import ISubsite
from plone import api
from plone.app.layout.viewlets import common
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class PathBarViewlet(common.PathBarViewlet):
    pathbar = ViewPageTemplateFile('pathbar.pt')

    def index(self):
        return self.pathbar()

    def get_subsite(self):
        nav_root = api.portal.get_navigation_root(self.context)
        if ISubsite.providedBy(nav_root):
            return dict(title=nav_root.Title(),
                        url=nav_root.absolute_url())
        else:
            return None
