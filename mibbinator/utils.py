from django.shortcuts import render_to_response
from django.template import RequestContext

def render(request, template, context={}):
	return render_to_response(template, context, context_instance=RequestContext(request))

def oidobj_sort(x, y):
    return oid_sort(x.oid, y.oid)

def oid_sort(x, y):
    xlist = x.split(".")
    ylist = y.split(".")
    while True:
	try:
	    curx = xlist.pop()
	except IndexError:
	    curx = None
	try:
	    cury = ylist.pop()
	except IndexError:
	    cury = None
	# first check for one OID being shorter
	# than the other - the longer one is bigger.
	if cury is None:
	    if curx is None:
		return 0
	    else:
		return 1
	if curx is None:
	    return -1
	# Otherwise, if the oid element is different,
	# the bigger OID element is bigger.
	if curx != cury:
	    return int(curx) - int(cury)
	# Otherwise, keep looping.
