## Controller Python Script "sendto"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=users_id=[], groups_id=[]
##title=Send an URL to a friend
##
REQUEST=context.REQUEST


from Products.CMFPlone.PloneTool import AllowSendto
from Products.CMFCore.utils import getToolByName
from ZODB.POSException import ConflictError
from Products.CMFPlone.utils import transaction_note

plone_utils = getToolByName(context, 'plone_utils')
mtool = getToolByName(context, 'portal_membership')
gtool = getToolByName(context, 'portal_groups')
site_properties = getToolByName(context, 'portal_properties').site_properties
pretty_title_or_id = plone_utils.pretty_title_or_id
empty_title = plone_utils.getEmptyTitle()

def getInnerMails(group):
   """Ottiene le mail degli utenti interni al gruppo,ricorsivamente nei gruppi interni"""
   retMail = []
   members = gtool.getGroupById(group.getId()).getGroupMembers()
   for m in members:
      if gtool.isGroup(m):
         # Gruppo interno: devo ottenere le mail di tutti gli utenti
         innerG = gtool.getGroupById(m.getId())
         retMail.extend(getInnerMails(innerG))
      else:
         # Utente comune
         email = m.getProperty("email") or None
         if email:
            retMail.append(email)
   return retMail

if not mtool.checkPermission(AllowSendto, context):
    return state.set(
            status='failure',
            portal_status_message='You are not allowed to send this link.')

at = getToolByName(context, 'portal_actions')
show = False
actions = at.listActionInfos(object=context)
# Check for visbility of sendto action
for action in actions:
    if action['id'] == 'sendto' and action['category'] == 'document_actions':
        show = True
if not show:
    return state.set(
        status='failure',
        portal_status_message='You are not allowed to send this link.')

# Find the view action.
context_state = context.restrictedTraverse("@@plone_context_state")
url = context_state.view_url()

theMailStrings = [x.strip() for x in REQUEST.send_to_address.split()]
host = context.MailHost
template = getattr(context, 'sendto_template')
encoding = context.portal_properties.site_properties.getProperty('default_charset', "UTF-8")
signature = context.portal_url.getPortalObject().getProperty('email_from_name')

### Utenti aggiuntivi
mtool = context.portal_membership
gtool = context.portal_groups
for u in users_id:
    email = mtool.getMemberById(u).getProperty("email") or None
    if email:
        theMailStrings.append(email)
### Gruppi aggiuntivi
for g in groups_id:
    members = gtool.getGroupById(g).getGroupMembers()
    for m in members:
        if gtool.isGroup(m):
            # Gruppo interno: devo ottenere le mail di tutti gli utenti
            innerG = gtool.getGroupById(m.getId())
            theMailStrings.extend(getInnerMails(innerG))
        else:
            # Utente comune
            email = m.getProperty("email") or None
            if email:
                theMailStrings.append(email)

kwargs = {'signature' : signature}

message = template(context, send_to_address=', '.join(theMailStrings),
    send_from_address=REQUEST.send_from_address,
    comment=REQUEST.get('comment', None), subject=pretty_title_or_id(context), **kwargs )

variables = {'send_from_address' : REQUEST.send_from_address,
             'send_to_address'   : REQUEST.send_to_address,#theMailStrings
             'subject'           : pretty_title_or_id(context),
             'url'               : url,
             'title'             : pretty_title_or_id(context),
             'description'       : context.Description(),
             'comment'           : REQUEST.get('comment', None),
             'envelope_from'     : site_properties.email_from_address
             }


try:
    #plone_utils.sendto( **variables )
    #host.secureSend(message, theMailStrings, REQUEST.send_from_address, subject=pretty_title_or_id(context), charset=encoding)
    for mail in theMailStrings:
        host.secureSend(message, mail, REQUEST.send_from_address, subject=pretty_title_or_id(context), charset=encoding)
    #pass
except ConflictError:
    raise
except: #XXX To many things could possibly go wrong. So we catch all.
    exception = context.plone_utils.exceptionString()
    message = context.translate("Unable to send mail: ${exception}",
                                {'exception': exception})
    return state.set(status='failure', portal_status_message=message)

tmsg='Sent page %s to %s' % (url, REQUEST.send_to_address)
transaction_note(tmsg)

return state.set(portal_status_message='Mail sent.')
