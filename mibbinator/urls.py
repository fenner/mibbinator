from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^mibbinator/', include('mibbinator.mib.urls')),
    (r'^comments/', include('django.contrib.comments.urls.comments')),
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^accounts/profile/', 'django.views.generic.simple.redirect_to', {'url': '/mibbinator/'}),
    (r'^accounts/', include('mibbinator.registration.urls')),
)
