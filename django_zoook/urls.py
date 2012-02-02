# -*- coding: utf-8 -*-
############################################################################################
#
#    Zoook. OpenERP e-sale, e-commerce Open Source Management Solution
#    Copyright (C) 2011 Zikzakmedia S.L. (<http://www.zikzakmedia.com>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
############################################################################################

from django.conf.urls.defaults import *
from django.contrib.sitemaps import GenericSitemap

from views import index
from settings import MEDIA_ROOT
from sitemaps import sitemaps
from transurl import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

js_info_dict = {
    'packages': ('django.conf',
                 'django.contrib.admin',
                ),
}

urlpatterns = patterns('',
    (r"^$", index),
    #~ catalog 
    (r"^%s/" % catalog_url['en'], include("catalog.urlsCatalog")),
    (r"^%s/"% catalog_url['es'], include("catalog.urlsCatalog")),
    (r"^%s/"% catalog_url['ca'], include("catalog.urlsCatalog")),
    
    #~ product 
    (r"^%s/" % product_url['en'], include("catalog.urlsProduct")),
    (r"^%s/" % product_url['es'], include("catalog.urlsProduct")),
    (r"^%s/" % product_url['ca'], include("catalog.urlsProduct")),
    
    #~ contact
    (r"^%s/" % contact_url['en'], include("contact.urlsContact")),
    (r"^%s/" % contact_url['es'], include("contact.urlsContact")),
    (r"^%s/" % contact_url['ca'], include("contact.urlsContact")),

#    (r"^search/", include("search.urlsSearch")),
    (r"^partner/", include("partner.urlsPartner")),
    (r"^sale/", include("sale.urlsSale")),
    (r"^account/", include("account.urlsAccount")),
    (r"^payment/", include("payment.urlsPayment")),

    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r"^static/(?P<path>.*)$", "django.views.static.serve", {"document_root": MEDIA_ROOT}),

    #~ Ajax Paths
    (r'^filemanager/', include('tools.filemanager.connector.urls')),
    (r'^inplaceeditform/', include('inplaceeditform.urls')),
    (r'^jsi18n$', 'django.views.i18n.javascript_catalog', js_info_dict),

    #~ Admin 
    (r'^manager/', include(admin.site.urls)),
    
    #~ Cms
    (r"^cms/", include("tools.cms.urlsCms")),

    # Content
    (r"^content/", include("content.urlsContent")),
    (r"^(?P<content>[^/]+)", include("content.urlsContent")),
)
