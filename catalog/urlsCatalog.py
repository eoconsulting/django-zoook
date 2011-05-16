from django.conf.urls.defaults import *
from catalog.views import *

"""Urls Catalog"""

urlpatterns = patterns("",
    (r'^$', 'catalog.views.index'),
    (r"^(?P<category>[^/]+)/$", 'catalog.views.category'),
#TODO: catagory/category
)
