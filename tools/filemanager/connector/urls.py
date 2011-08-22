from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^dirlist/$', 'tools.filemanager.connector.views.dirlist'),
    (r'^$', 'tools.filemanager.connector.views.handler'),
)
