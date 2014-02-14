from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to
import views

urlpatterns = patterns('',
    (r'^$', views.home),
    # would like to avoid hardcoding mibbinator here
    (r'^(o/\.|\.?)(?P<oid>[0-9.]*)$', redirect_to, { 'url': '/mibbinator/o/%(oid)s' }),
    (r'^o/(?P<oid>[0-9.]+)$', views.byoid),
    (r'^m/(?P<module>[\w-]+)$', views.bymodule),
    (r'^(?P<name>\w+)$', views.byname),
)
