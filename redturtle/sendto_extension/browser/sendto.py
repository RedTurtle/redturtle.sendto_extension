# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from redturtle.sendto_extension import _


class SendtoExtensionView(BrowserView):
    """Service view for the send_to extension"""

    i18n_send_to_address = _('Send to')
    i18n_send_to_address_help =  _('Enter a list of email addresses to send this page to')
    i18n_send_to_members = _('Send to site members')
    i18n_send_to_members_help =  _('Select a set of site members to send this page to')
    i18n_send_to_groups = _('Send to groups')
    i18n_send_to_groups_help = _('Select a set of groups to which members send this page to')
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
        request.set('disable_border', 1)

    def _send(self):
        """Send e-mail to all recipients, loading e-mail from member is needed and doing security check"""
        form = self.request.form
        # TODO: to be done

    def __call__(self):
        if self.request.form.get('form.submitted'):
            import pdb;pdb.set_trace()
            self._send()
        return self.index()
