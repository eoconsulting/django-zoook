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

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.utils.translation import get_language
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site

from settings import *
from tools.conn import conn_webservice
from tools.zoook import connOOOP, siteConfiguration

from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.ipn.models import PayPalIPN

from sale.email import SaleOrderEmail

import time
import logging

@login_required
def index(request):
    """
    Paypal
    OpenERP Payment Type App is: paypal
    """
    
    logging.basicConfig(filename=LOGSALE,level=logging.INFO)

    if not 'sale_order' in request.session:
        error = _('Order number is not available. Use navigation menu.')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    conn = connOOOP()
    if not conn:
        error = _('Error when connecting with our ERP. Try again or cantact us')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    payment_type = conn.ZoookSaleShopPaymentType.filter(app_payment='paypal')
    orders = conn.SaleOrder.filter(name=request.session['sale_order'])
        
    if (len(payment_type) > 0) and len(orders) > 0:
        #change payment_type = done
        order = orders[0]
        order.payment_state = 'done'
        order.save()

        site = Site.objects.get_current()
        site_configuration = siteConfiguration(SITE_ID)

        paypal_dict = {
            "business": PAYPAL_RECEIVER_EMAIL,
            "amount": order.amount_total,
            "item_name": site_configuration.site_title,
            "invoice": order.name,
            "currency_code": PAYPAL_CURRENCY,
            "notify_url": "http://%s%s" % (site.domain, '/payment/paypal/ipn'),
            "return_url": "http://%s%s" % (site.domain, '/saas/invoice/confirm'),
            "cancel_return": "http://%s%s" % (site.domain, '/payment/paypal/error'),
        }

        form = PayPalPaymentsForm(initial=paypal_dict)
        logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), 'Order %s: paypal form and redirect' % (order.name) ))
        return render_to_response("paypal/form.html", {'form':form, 'debug':DEBUG}, context_instance=RequestContext(request))

    else:
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

@login_required
def paypal_error(request):
    """
    Error Paypal view
    """

    error = _('Error return Paypal Payment. Go to sale orders and repeat payment')
    return HttpResponse(render_to_response('paypal/error.html', {'error':error}, context_instance=RequestContext(request)))

@login_required
def paypal_confirm(request):
    """
    Confirmation Paypal view
    """

    logging.basicConfig(filename=LOGSALE,level=logging.INFO)

    conn = connOOOP()
    order = request.session['sale_order']

    #TODO: check real IPN and test this code
    payment_paypal = PayPalIPN.objects.filter(invoice=order)
    payment = False

    if len(payment_paypal)>0:
        if (payment_paypal[0].verify_sign):
            payment = True

    orders = conn.SaleOrder.filter(name=request.session['sale_order'])

    if payment and len(orders) > 0:
        order = orders[0]
        payment_order = conn_webservice('sale.order', 'sale_order_payment', [order.name, 'paypal'])

        values = {'order':request.session['sale_order']}
        del request.session['sale_order']

        #send email sale order
        SaleOrderEmail(order.id)

        logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), 'Order %s: paypal payment finish' % (order.name) ))

        return HttpResponse(render_to_response('paypal/confirm.html', values, context_instance=RequestContext(request)))
    else:
        error = _('Error return Paypal Payment. Contact us to check payment')
        return HttpResponse(render_to_response('paypal/error.html', {'error':error}, context_instance=RequestContext(request)))
