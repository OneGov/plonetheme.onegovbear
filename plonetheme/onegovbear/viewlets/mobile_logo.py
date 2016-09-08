from plone import api
from plone.app.layout.viewlets.common import LogoViewlet
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class MobileLogo(LogoViewlet):
    index = ViewPageTemplateFile('mobile_logo.pt')

    def available(self):
        """Grap a logo thru acquistion"""
        return bool(getattr(self.context, 'mobile_logo.png', False))

    def update(self):
        super(MobileLogo, self).update()
        self.url = api.portal.get().absolute_url()
        self.title = api.portal.get().Title()
