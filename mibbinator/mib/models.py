from django.db import models

class Restriction(models.Model):
    name = models.CharField(maxlength=30)
    description = models.CharField(maxlength=255, blank=True)
    public = models.BooleanField()
    notes = models.TextField(blank=True)
    def __str__(self):
	return self.name
    class Admin:
	pass

class Module(models.Model):
    module = models.CharField(maxlength=100, unique=True)
    source = models.CharField(maxlength=100, blank=True)
    srcstat = models.CharField(maxlength=20, blank=True)	# this was an enum in the original
    xdate = models.DateTimeField(null=True, blank=True)
    contact = models.TextField(blank=True)
    lastrevised = models.DateTimeField(null=True, blank=True)
    smidump = models.TextField()
    org = models.CharField(maxlength=255, blank=True)
    copyright = models.TextField(blank=True)
    restriction = models.ForeignKey(Restriction, null=True, blank=True)
    def __str__(self):
	return self.module
    class Admin:
        pass

class Object(models.Model):
    object = models.CharField(maxlength=100)
    module = models.ForeignKey(Module)
    type = models.CharField(maxlength=20)
    syntax = models.TextField(blank=True)
    access = models.CharField(maxlength=50, blank=True)
    units = models.CharField(maxlength=50, blank=True)
    displayhint = models.CharField(maxlength=50, blank=True)
    status = models.CharField(maxlength=50, blank=True)
    oid = models.CharField(maxlength=255, blank=True)
    description = models.TextField(blank=True)
    reference = models.TextField(blank=True)
    defval = models.TextField(blank=True)	# seems odd but can have long enumerations/bits
    def save(self):
	super(Object, self).save()
	parent = ".".join(self.oid.split(".")[:-1])
	OID.objects.get_or_create(oid=self.oid, parent=parent)
    class Meta:
	unique_together=(('module', 'object'),)

class Import(models.Model):
    '''Forward references are represented by `Module::obJecTnaMe`
    in `imp`.'''
    module = models.ForeignKey(Module)
    imp = models.CharField(maxlength=255, blank=True)
    srcmod = models.ForeignKey(Module, related_name='imported_by', null=True)
    object = models.ForeignKey(Object, related_name='imported_by', null=True)
    class Meta:
        unique_together=(('module','imp'), )

class OID(models.Model):
    oid = models.CharField(maxlength=255, unique=True)
    # object's null=True is just for development, until I figure out
    # the algorithm for "which of several oids is the real one"
    object = models.ForeignKey(Object, related_name='primary_oid', null=True)
    parent = models.CharField(maxlength=255)
