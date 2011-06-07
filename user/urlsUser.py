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
from user.views import *

"""Urls User"""
urlpatterns = patterns("",
    (r'^$', 'user.views.login'),
    (r'^login', 'user.views.login'),
    (r'^profile', 'user.views.profile'),
    #~ (r'^profile', 'sale.views.orders'),
    (r"^logout/$", "django.contrib.auth.views.logout", {"next_page":"/user/"}),
    (r'^register', 'user.views.register'),
    (r'^remember', 'user.views.remember'),
    (r'^changepassword', 'user.views.changepassword'),
    (r'^partner', 'user.views.partner'),
)
