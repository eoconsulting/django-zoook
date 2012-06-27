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

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.utils.translation import get_language
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site

from django_zoook.settings import *
from django_zoook.tools.conn import conn_webservice
from django_zoook.tools.zoook import connOOOP, siteConfiguration

from sermepa.sermepa.forms import SermepaPaymentForm
from sermepa.sermepa.models import SermepaResponse

from django_zoook.sale.email import SaleOrderEmail

import logging

@login_required
def index(request):
    """
    Sermepa (Servired)
    OpenERP Payment Type App is: sermepa
    Sale Order Reference:
        - Only numbers, not SO0001
        - Minimium 4, Maximun 12
    """

    title = _(u'Payment Credit Card Servired')

    if not 'sale_order' in request.session:
        error = _('Order number is not available. Use navigation menu.')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    conn = connOOOP()
    if not conn:
        error = _('Error when connecting with our ERP. Try again or cantact us.')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    payment_type = conn.ZoookSaleShopPaymentType.filter(app_payment='sermepa')
    orders = conn.SaleOrder.filter(name=request.session['sale_order'])
        
    if (len(payment_type) > 0) and len(orders) > 0:
        #change payment_type = done
        order = orders[0]
        order.payment_state = 'done'
        order.save()

        site = Site.objects.get_current()
        site_configuration = siteConfiguration(SITE_ID)

        sermepa_dict = {
            "Ds_Merchant_Titular": SERMEPA_MERCHANT_NAME,
            "Ds_Merchant_MerchantData": '',
            "Ds_Merchant_MerchantName": SERMEPA_MERCHANT_NAME,
            "Ds_Merchant_ProductDescription": site_configuration.site_title,
            "Ds_Merchant_Amount": int(order.amount_total* 100),
            "Ds_Merchant_TransactionType": SERMEPA_TRANS_TYPE,
            "Ds_Merchant_Terminal": SERMEPA_TERMINAL,
            "Ds_Merchant_MerchantCode": SERMEPA_MERCHANT_CODE,
            "Ds_Merchant_Order": order.name,
            "Ds_Merchant_Currency": SERMEPA_CURRENCY,
            "Ds_Merchant_MerchantURL": SERMEPA_MERCHANT_URL,
            "Ds_Merchant_UrlOK": "http://%s%s" % (site.domain, '/payment/sermepa/confirm'),
            "Ds_Merchant_UrlKO": "http://%s%s" % (site.domain, '/payment/sermepa/error'),
        }

        form = SermepaPaymentForm(initial=sermepa_dict)
        debug = DEBUG
        logging.info('Order %s: sermepa form and redirect' % order.name)
        return HttpResponse(render_to_response('sermepa/form.html', locals(), context_instance=RequestContext(request)))

    else:
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

@login_required
def sermepa_error(request):
    """
    Error Sermepa view
    """

    title = _(u'Error Payment Credit Card Servired')
    error = _(u'Error return Servired Payment. Go to sale orders and repeat payment')
    return HttpResponse(render_to_response('sermepa/error.html', {'error':error}, context_instance=RequestContext(request)))

@login_required
def sermepa_confirm(request):
    """
    Confirmation Sermepa view
    """

    title = _(u'Confirmation Credit Card Servired')

    conn = connOOOP()
    order = request.session['sale_order']

    #TODO: check real IPN and test this code
    payment_sermepa = SermepaResponse.objects.filter(Ds_Order=order)
    payment = False

    if len(payment_sermepa)>0:
        if (payment_sermepa[0].Ds_Signature):
            payment = True

    orders = conn.SaleOrder.filter(name=request.session['sale_order'])

    if payment and len(orders) > 0:
        order = orders[0]
        payment_order = conn_webservice('sale.order', 'sale_order_payment', [order.name, 'sermepa'])

        values = {'order':request.session['sale_order']}
        del request.session['sale_order']

        #send email sale order
        SaleOrderEmail(order.id)

        logging.info(_('Order %s: servired payment finish') % order.name)

        return HttpResponse(render_to_response('sermepa/confirm.html', values, context_instance=RequestContext(request)))
    else:
        error = _('Error return Servired Payment. Contact us to check payment')
        return HttpResponse(render_to_response('sermepa/error.html', {'error':error}, context_instance=RequestContext(request)))
