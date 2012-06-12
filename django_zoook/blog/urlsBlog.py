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
from django_zoook.blog.views import *
from django_zoook.blog.feeds import *

"""Urls Blog"""

urlpatterns = patterns("",
    url(r'^$', 'django_zoook.blog.views.blog_list', name='blog_list'),
    url(r"^edit/(?P<blog_id>[^/]+)", 'django_zoook.blog.views.blog_edit', name='blog_edit'),
    url(r"^add/", 'django_zoook.blog.views.blog_add', name='blog_add'),
    url(r"^key/(?P<key>[^/]+)/", 'django_zoook.blog.views.blog_list', name='blog_key'),
    url(r"^rss/$", BlogFeed()),
    url(r"^(?P<blog>[^/]+)", 'django_zoook.blog.views.blog_detail', name='blog_blog'),
)
