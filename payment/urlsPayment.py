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

"""Urls Payments"""
urlpatterns = patterns("",
    #~ Sermepa Payment
    #~ (r'^sermepa/error', 'payment.sermepa.views.sermepa_error'),
    #~ (r'^sermepa/confirm', 'payment.sermepa.views.sermepa_confirm'),
    #~ (r'^sermepa/ipn', include('sermepa.sermepa.urls')),
    #~ (r'^sermepa/', 'payment.sermepa.views.index'),

    #~ Paypal Payment
    #~ (r'^paypal/error', 'payment.paypal.views.paypal_error'),
    #~ (r'^paypal/confirm', 'payment.paypal.views.paypal_confirm'),
    #~ (r'^paypal/ipn', include('paypal.standard.ipn.urls')),
    #~ (r'^paypal/', 'payment.paypal.views.index'),
    
    #~ Check Payment
    #~ (r"^check/", 'payment.check.views.index'),

    #~ CashOnDelivery
    #~ (r"^cashondelivery/", 'payment.cashondelivery.views.index'),

    #~ Debit
    #~ (r"^debit/confirm", 'payment.debit.views.confirm'),
    #~ (r"^debit/", 'payment.debit.views.index'),
)
