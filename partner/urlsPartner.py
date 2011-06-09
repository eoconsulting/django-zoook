# -*- encoding: utf-8 -*-
############################################################################################
#
#    Zoook e-sale for OpenERP, Open Source Management Solution	
#    Copyright (C) 2011 Zikzakmedia S.L. (<http://www.zikzakmedia.com>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
############################################################################################

from django.conf.urls.defaults import *
from partner.views import *

"""Urls Partner"""
urlpatterns = patterns("",
    (r'^$', 'partner.views.login'),
    (r'^login', 'partner.views.login'),
    (r'^profile', 'partner.views.profile'),
    #~ (r'^profile', 'sale.views.orders'),
    (r"^logout/$", "django.contrib.auth.views.logout", {"next_page":"/partner/"}),
    (r'^register', 'partner.views.register'),
    (r'^remember', 'partner.views.remember'),
    (r'^changepassword', 'partner.views.changepassword'),
    (r'^partner', 'partner.views.partner'),
)
