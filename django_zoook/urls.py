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

import re

from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib.sitemaps import GenericSitemap

from django_zoook.views import index, doc
from django_zoook.search.views import search
from django_zoook.tag.views import keyword
from django_zoook.sitemaps import sitemaps
from django_zoook.transurl import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

js_info_dict = {
    'packages': ('django.conf',
                 'django.contrib.admin',
                ),
}

urlpatterns = patterns('',
    #url(r"^$", index, name='index'),
    url(r"^$", doc, name='index'),

    # catalog 
    url(r"^%s/" % catalog_url['en'], include("django_zoook.catalog.urlsCatalog")),
    url(r"^%s/"% catalog_url['es'], include("django_zoook.catalog.urlsCatalog")),
    url(r"^%s/"% catalog_url['ca'], include("django_zoook.catalog.urlsCatalog")),

    # catalog manage
    url(r'^catalogmanage/', include('django_zoook.catalog.urlsCatalogManage')),

    # manufacturer 
    url(r"^%s/" % manufacturer_url['en'], include("django_zoook.catalog.urlsManufacturer")),
    url(r"^%s/" % manufacturer_url['es'], include("django_zoook.catalog.urlsManufacturer")),
    url(r"^%s/" % manufacturer_url['ca'], include("django_zoook.catalog.urlsManufacturer")),

    # product 
    url(r"^%s/" % product_url['en'], include("django_zoook.catalog.urlsProduct")),
    url(r"^%s/" % product_url['es'], include("django_zoook.catalog.urlsProduct")),
    url(r"^%s/" % product_url['ca'], include("django_zoook.catalog.urlsProduct")),

    # contact
    url(r"^%s/" % contact_url['en'], include("django_zoook.contact.urlsContact")),
    url(r"^%s/" % contact_url['es'], include("django_zoook.contact.urlsContact")),
    url(r"^%s/" % contact_url['ca'], include("django_zoook.contact.urlsContact")),

    # Search
    #url(r'^search/', include('haystack.urls')),
    url(r"^search", search, name='search'),

    # Tag
    url(r"^tag/(?P<tag>[^/]+)/$", keyword, name='tag'),

    url(r"^partner/", include("django_zoook.partner.urlsPartner")),
    url(r"^sale/", include("django_zoook.sale.urlsSale")),
    url(r"^account/", include("django_zoook.account.urlsAccount")),
    url(r"^payment/", include("django_zoook.payment.urlsPayment")),
    url(r"^base/", include("django_zoook.base.urlsBase")),

    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),

    # Ajax Paths
    url(r'^filemanager/', include('django_zoook.tools.filemanager.connector.urls')),
    url(r'^inplaceeditform/', include('inplaceeditform.urls')),
    url(r'^jsi18n$', 'django.views.i18n.javascript_catalog', js_info_dict),

    # Admin 
    url(r'^manager/', include(admin.site.urls)),
    url(r'^filebrowser/', include('filebrowser.urls')),

    #  Blog
    url(r"^blog/", include("django_zoook.blog.urlsBlog")),

    # Cms
    url(r"^cms/", include("django_zoook.tools.cms.urlsCms")),

    # Content
    url(r"^content/", include("django_zoook.content.urlsContent")),
)

if settings.STATICFILES_IGNORE_DEBUG:
    urlpatterns += patterns('',
            url(r'^%s(?P<path>.*)$' % re.escape(settings.STATIC_URL.lstrip('/')), 'staticsfiles_ignoredebug.views.serve'),
        )
