## Script (Python) "searchAdvancedForMembers"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=query
##title=
##
mtool = context.portal_membership

queryStrings = query.split()

results = []

if queryStrings:
    for qs in queryStrings:
        found = mtool.searchForMembers(name=qs)
        if found:
            results.extend(found)
else:
    results = mtool.searchForMembers(name=query)    

# controllo ed elimino duplicati
rstmp = {}

for r in results:
    rstmp[r.getId()]=r

return rstmp.values()
