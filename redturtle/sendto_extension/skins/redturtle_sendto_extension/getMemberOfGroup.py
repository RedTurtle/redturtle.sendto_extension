## Script (Python) "getMemberOfGroup"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=groupid
##title=
##

gtool = context.portal_groups
mtool = context.portal_membership

group = gtool.getGroupById(groupid)

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
