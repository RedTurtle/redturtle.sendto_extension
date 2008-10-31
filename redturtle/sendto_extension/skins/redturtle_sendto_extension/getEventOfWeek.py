## Script (Python) "getEventOfWeek"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=limit=10
##title=Struttura degli eventi della settimana
##

from DateTime import DateTime

now = DateTime()
dow = DateTime().dow()

start_day = now-dow+1
end_day = now+(7-dow)

#Start nell'intervallo
results = context.portal_catalog.searchResults(
                             Type="Event",
                             start = { "query" : [start_day,end_day], 
                                       "range" : "minmax" },
                             end = { "query" : [end_day,], 
                                     "range" : "min" },
                             review_state=['published','highlights'],
)

#End nell'intervallo
results2 = context.portal_catalog.searchResults(
                             Type="Event",
                             end = { "query" : [start_day,end_day], 
                                       "range" : "minmax" },
                             start = { "query" : [start_day,], 
                                       "range" : "max" },
                             review_state=['published','highlights'],
)

#Start minore di start_day e End maggiore di end_day
results3 = context.portal_catalog.searchResults(
                             Type="Event",
                             start = { "query" : [start_day,], 
                                       "range" : "max" },
                             end = { "query" : [end_day,], 
                                       "range" : "min" },
                             review_state=['published','highlights'],
)

#Start e End nell'intervallo
results4 = context.portal_catalog.searchResults(
                             Type="Event",
                             start = { "query" : [start_day,end_day], 
                                       "range" : "minmax" },
                             end = { "query" : [start_day,end_day], 
                                       "range" : "minmax" },
                             review_state=['published','highlights'],
)

restot = [x for x in results] + [x for x in results2] + [x for x in results3] + [x for x in results4]

def event_compare(x, y):
    if x.end > y.end:
       return 1
    elif x.end == y.end:
       return 0
    else: # x.end<y.end
       return -1

#for x in restot:
#   print x.Title, x.start, x.end

#return printed

restot.sort(event_compare)

if limit:
    return restot[:limit]

return restot
 
