# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from plone.memoize.instance import memoize

class SendtoExtensionView(BrowserView):
    """Service view for the send_to extension"""
    
    def listGroups(self):
        gtool = getToolByName(self.context, 'portal_groups')
        return gtool.listGroups()


    def getMemberOfGroup(self, group_id):
        """Given a group id, return its members.
        @return: a list of couples member_id, fullname.
        """
        import pdb;pdb.set_trace()
        gtool = getToolByName(self.context, 'portal_groups')
        mtool = getToolByName(self.context, 'portal_membership')
        group = gtool.getGroupById(group_id)
        members = group.getGroupMembers()
        lst = []
        for m in members:
            mdata = [m.getId()]
            name = m.getProperty('fullname', None)
            if name:
                mdata.append(" (%s)" % name)
            else:
                mdata.append("")
            lst.append(mdata)
        return lst

    def default_addme_value(self):
        """The default value for this site for the addme check
        @return: False, or the string "checked"
        """
        try:
            addme_to_cc_default = self.context.portal_properties.site_properties.addme_to_cc_default
        except AttributeError:
            addme_to_cc_default = False
        return (addme_to_cc_default and 'checked') or False

