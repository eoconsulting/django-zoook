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

"""Urls Payments"""
urlpatterns = patterns("",
    # Sermepa Payment
    # url(r'^sermepa/error', 'django_zoook.payment.sermepa.views.sermepa_error', name='payment_sermepa_error'),
    # url(r'^sermepa/confirm', 'django_zoook.payment.sermepa.views.sermepa_confirm', name='payment_sermepa_confirm'),
    # url(r'^sermepa/ipn', include('sermepa.sermepa.urls'), name='payment_sermepa_ipn'),
    # url(r'^sermepa/', 'django_zoook.payment.sermepa.views.index', name='payment_sermepa'),

    # Paypal Payment
    # url(r'^paypal/error', 'django_zoook.payment.paypal.views.paypal_error', name='payment_paypal_error'),
    # url(r'^paypal/confirm', 'django_zoook.payment.paypal.views.paypal_confirm', name='payment_paypal_confirm'),
    # url(r'^paypal/ipn', include('paypal.standard.ipn.urls'), name='payment_paypal_ipn'),
    # url(r'^paypal/', 'django_zoook.payment.paypal.views.index', name='payment_paypal'),

    # Check Payment
    # url(r"^check/", 'django_zoook.payment.check.views.index', name='payment_check'),

    # Bank Transfer Payment
    # url(r"^banktransfer/", 'django_zoook.payment.banktransfer.views.index', name='payment_banktransfer'),

    # CashOnDelivery
    url(r"^cashondelivery/", 'django_zoook.payment.cashondelivery.views.index', name='payment_cashondelivery'),

    # Debit
    # url(r"^debit/confirm", 'django_zoook.payment.debit.views.confirm', name='payment_debit_confirm'),
    # url(r"^debit/", 'django_zoook.payment.debit.views.index', name='payment_debit'),

    # 4b
    # url(r'^pasat4b/error', 'django_zoook.payment.pasat4b.views.pasat4b_error', name='payment_pasat4b_error'),
    # url(r'^pasat4b/confirm', 'django_zoook.payment.pasat4b.views.pasat4b_confirm', name='payment_pasat4b_confirm'),
    # url(r'^pasat4b/getorder', 'django_zoook.payment.pasat4b.views.pasat4b_getorder', name='payment_pasat4b_getorder'),
    # url(r'^pasat4b/ipn', include('pasat4b.pasat4b.urls'), name='payment_pasat4b_ipn'),
    # url(r'^pasat4b/', 'django_zoook.payment.pasat4b.views.index', name='payment_pasat4b'),
    )
