# -*- encoding: utf-8 -*-
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

"""Urls Sale"""

urlpatterns = patterns("",
    (r'^$', 'sale.views.orders'),
    (r'^payment/(?P<order>[^/]+)$', 'sale.views.payment'),
    (r"^order/(?P<order>[^/]+)$", 'sale.views.order'),
    (r"^checkout/remove/(?P<code>[^/]+)$", 'sale.views.checkout_remove'),
    (r"^checkout/confirm/", 'sale.views.checkout_confirm'),
    (r"^checkout/", 'sale.views.checkout'),
)
