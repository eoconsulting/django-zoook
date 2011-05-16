from django.conf.urls.defaults import *
from catalog.views import *

"""Urls Product"""

urlpatterns = patterns("",
    (r"^(?P<product>[^/]+)$", 'catalog.views.product'),
)
