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
from django_zoook.partner.views import *

"""Urls Partner"""
urlpatterns = patterns("",
    url(r'^$', 'django_zoook.partner.views.login', name='partner'),
    url(r'^login', 'django_zoook.partner.views.login', name='partner_login'),
    url(r'^profile', 'django_zoook.partner.views.profile', name='partner_profile'),
    #url(r'^profile', 'django_zoook.sale.views.orders'),
    url(r"^logout/$", "django.contrib.auth.views.logout", {"next_page":"/"}, name='partner_logout'),
    url(r'^register', 'django_zoook.partner.views.register', name='partner_register'),
    url(r'^remember', 'django_zoook.partner.views.remember', name='partner_remember'),
    url(r'^changepassword', 'django_zoook.partner.views.changepassword', name='partner_changepassword'),
    url(r'^partner', 'django_zoook.partner.views.partner', name='partner_partner'),
)
