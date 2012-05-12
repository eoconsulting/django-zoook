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
    (r'^$', 'django_zoook.partner.views.login','', 'partner_index'),
    (r'^login', 'django_zoook.partner.views.login', '', 'auth_login'),
    (r'^profile', 'django_zoook.partner.views.profile'),
    #~ (r'^profile', 'django_zoook.sale.views.orders'),
    (r"^logout/$", "django.contrib.auth.views.logout", {"next_page":"/"}, 'auth_logout'),
    (r'^register', 'django_zoook.partner.views.register', '', 'auth_register'),
    (r'^remember', 'django_zoook.partner.views.remember', '' , 'auth_remember'),
    (r'^changepassword', 'django_zoook.partner.views.changepassword', '', 'auth_changepassword'),
    (r'^partner', 'django_zoook.partner.views.partner','','partner_partner'),
)
