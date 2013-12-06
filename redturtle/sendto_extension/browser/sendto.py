# -*- coding: utf-8 -*-

from zope.component import queryUtility, getMultiAdapter
from Products.Five import BrowserView
from plone.registry.interfaces import IRegistry
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from redturtle.sendto_extension import _
from redturtle.sendto_extension.interfaces import ISendtoExtensionSettings


class SendtoExtensionView(BrowserView):
    """Service view for the send_to extension"""

    i18n_send_to_address = _('Send to')
    i18n_send_to_address_help =  _('Enter a list of email addresses to send this page to')
    i18n_send_to_address_bcc = _('Send to (using BCC)')
    i18n_send_to_address_help_bcc =  _('i18n_send_to_address_help_bcc',
                                       default=u'Enter a list of email addresses to send this page to.\n'
                                               u'Addresses in this list will not be revealed to other recipients')
    i18n_send_to_members = _('Send to site members')
    i18n_send_to_members_help =  _('send_to_members_help',
                                   default=u'Select a set of site members to send this page to.\n'
                                           u'Start typing some character, then select from the dropdown.')
    i18n_send_to_groups = _('Send to groups')
    i18n_send_to_groups_help = _('send_to_groups_help',
                                 u'Select a set of groups to which members send this page to.\n'
                                 u'Start typing some character, then select from the dropdown.')
    i18n_send_to_members_bcc = _('Send to site members (using BCC)')
    i18n_send_to_members_help_bcc =  _('send_to_members_help_bcc',
                                       default=u'Select a set of site members to send this page to.\n'
                                               u'Start typing some character, then select from the dropdown.\n'
                                               u'Users in this list will not be revealed to other recipients')
    i18n_send_to_groups_bcc = _('Send to groups (using BCC)')
    i18n_send_to_groups_help_bcc = _('send_to_groups_help_bcc',
                                     default=u'Select a set of groups to which members send this page to.\n'
                                             u'Start typing some character, then select from the dropdown.\n'
                                             u'Users inside groups in this list will not be revealed to other recipients')
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
        request.set('disable_border', 1)

    def __call__(self):
        if self.request.form.get('form.submitted') and self.send():
            return self.request.response.redirect(
                    self.context.absolute_url() + '/@@' + self.__name__)
        return self.index()

    def _members_email(self, members_id):
        acl_users = getToolByName(self.context, 'acl_users')
        emails = []
        for member_id in members_id:
            member_data = acl_users.searchUsers(name=member_id, exact_match=True)
            if len(member_data)>0:
                member = acl_users.getUserById(member_data[0].get('login'))
                if member.getProperty('email'):
                    emails.append(member.getProperty('email'))
        return emails

    def _groups_email(self, groups_id):
        acl_users = getToolByName(self.context, 'acl_users')
        emails = []
        for group_id in groups_id:
            group_data = acl_users.searchGroups(name=group_id, exact_match=True)
            if len(group_data)>0:
                group = acl_users.getGroupById(group_data[0].get('groupid'))
                if group.getProperty('email'):
                    emails.append(group.getProperty('email'))
                # Now emails from users
                emails.extend(self._members_email(group.getGroupMemberIds()))
        return emails

    def send(self):
        """Send e-mail to all recipients, loading e-mail from member is needed and doing security check"""
        form = self.request.form
        sender = form.get('send_from_address', None)
        message = form.get('message', '')
        send_to_address = form.get('send_to_address', [])
        send_to_address_bcc = form.get('send_to_address_bcc', [])
        send_to_members = form.get('send_to_members', [])
        send_to_members_bcc = form.get('send_to_members_bcc', [])
        send_to_groups = form.get('send_to_groups', [])
        send_to_groups_bcc = form.get('send_to_groups_bcc', [])
        cc_me = form.get('cc_me', False)
        
        # If we have items in both a list and in the bcc version, remove from the list
        send_to_address = [x for x in send_to_address if x not in send_to_address_bcc]
        send_to_members = [x for x in send_to_members if x not in send_to_members_bcc]
        send_to_groups = [x for x in send_to_groups if x not in send_to_groups_bcc]

        # get email from principals
        members_email = self._members_email(send_to_members)
        members_email_bcc = self._members_email(send_to_members_bcc)
        groups_email = self._groups_email(send_to_groups)
        groups_email_bcc = self._members_email(send_to_groups_bcc)
        if cc_me:
            member = getToolByName(self.context, 'portal_membership').getAuthenticatedMember()
            members_email.append(member.getProperty('email'))

        return self._send_mail(sender=sender,
                               message=message,
                               to=send_to_address + members_email + groups_email,
                               bcc=send_to_address_bcc + send_to_members_bcc + send_to_groups_bcc,
                               )

    def _repl_interpolation(self, text, sender, message):
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        portal = portal_state.portal()
        portal_url = portal_state.portal_url()
        text = text.replace('${site_name}', portal.title_or_id().decode('utf-8'))
        text = text.replace('${site_description}', portal.getProperty('description').decode('utf-8'))
        text = text.replace('${site_url}', portal_url.decode('utf-8'))
        text = text.replace('${title}', self.context.title_or_id().decode('utf-8'))
        text = text.replace('${url}', self.context.absolute_url().decode('utf-8'))
        text = text.replace('${sender}', sender.decode('utf-8'))
        # message intentation
        message = "\n".join(['\t'+x for x in message.strip().splitlines()])
        text = text.replace('${comment}', message)
        return text

    def _send_mail(self, sender, message, to=[], bcc=[]):
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(ISendtoExtensionSettings, check=False)
        subject = settings.email_subject
        body = settings.email_body
        subject = self._repl_interpolation(subject, sender, '')
        body = self._repl_interpolation(body, sender, message)
        mail_host = getToolByName(self.context, 'MailHost')
        to = [x for x in to if mail_host.validateSingleEmailAddress(x) and x not in bcc]
        bcc = [x for x in bcc if mail_host.validateSingleEmailAddress(x)]
        ptool = getToolByName(self.context, 'plone_utils')
        if not sender:
             ptool.addPortalMessage(_('No sender address provided'), type="error")
             return False
        if not to and not bcc:
             ptool.addPortalMessage(_('No recipients'), type="error")
             return False
        mail_host.secureSend(body, to, sender, subject=subject,
                             mbcc=bcc, subtype='plain', charset='utf-8')
        ptool.addPortalMessage(_('Message sent'))
        return True
