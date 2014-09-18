## Controller Validator "validate_sendto"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=send_to_address='',send_from_address='', users_id=None, groups_id=None, recaptcha_response_field=''
##title=validates the email adresses
##
plone_utils=context.plone_utils

if context.restrictedTraverse('@@plone_portal_state').anonymous():
    recaptcha_verify = context.restrictedTraverse('@@captcha/verify', None)
    if recaptcha_verify:
        try:
            if not recaptcha_verify():
                state.setError('recaptcha_response_field', 'Il codice di protezione captcha è errato. Prego riprova')
        except ValueError:
            pass

if not send_to_address and not users_id and not groups_id:
    state.setError('send_to_address', 'Please submit an email address.', 'email_required')

send_to_address = send_to_address.split()
if same_type(send_to_address,[]):
    for m in send_to_address:
        if not plone_utils.validateEmailAddresses(m):
            state.setError('send_to_address', 'Please submit a valid email address.', 'email_required')
else:
    if not plone_utils.validateEmailAddresses(send_to_address):
        state.setError('send_to_address', 'Please submit a valid email address.', 'email_required')

if not send_from_address:
    state.setError('send_from_address', 'Please submit an email address.', 'email_required')

if not plone_utils.validateSingleEmailAddress(send_from_address):
    state.setError('send_from_address', 'Please submit a valid email address.', 'email_required')

if state.getErrors():
    return state.set(status='failure', portal_status_message='Please correct the indicated errors.')
else:
    return state
