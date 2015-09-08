from plone.app.layout.viewlets import common
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class OneGovBearSkipLinksViewlet(common.SkipLinksViewlet):
    index = ViewPageTemplateFile('accesskeys.pt')
