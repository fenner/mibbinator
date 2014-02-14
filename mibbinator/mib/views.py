from django.shortcuts import get_object_or_404
from mibbinator.utils import render, oidobj_sort
from models import Object, Module, OID

def home(request):
    # collect site news?
    return render(request, 'home.html')

def byoid(request, oid):
    # look up oid matches
    objects = Object.objects.filter(oid=oid)
    parent = ".".join(oid.split(".")[:-1])
    try:
	thisoid = OID.objects.get(oid=oid)
    except:
	thisoid = None
    children = list(OID.objects.filter(parent=oid))
    children.sort(oidobj_sort)
    childoidlist = [child.oid for child in children]
    namedict = {}
    for entry in Object.objects.filter(oid__in=childoidlist).distinct().values('oid','object'):
	if not namedict.has_key(entry['oid']):
	    namedict[entry['oid']] = []
	namedict[entry['oid']].append(entry['object'])
    for child in children:
	if namedict.has_key(child.oid):
	    child.names = namedict[child.oid]
    return render(request, 'oidbrowse.html', {'oid': oid, 'objects': objects, 'parent': parent, 'children': children, 'thisoid': thisoid})

def byname(request, name):
    try:
	object = Object.objects.get(object=name)
    except Object.DoesNotExist:
	object = None
    if object:
	parent = ".".join(object.oid.split(".")[:-1])
	objects = Object.objects.filter(oid=object.oid)
    return render(request, 'byname.html', {'object': object, 'objects': objects, 'parent': parent})

def bymodule(request, module):
    module = get_object_or_404(Module, module=module)
    return render(request, 'module.html', {'module': module})
