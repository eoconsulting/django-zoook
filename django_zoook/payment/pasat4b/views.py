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

from pasat4b.pasat4b.forms import pasat4bPaymentForm
from pasat4b.pasat4b.models import pasat4bResponse

from django_zoook.sale.email import SaleOrderEmail

import logging

@login_required
def index(request):
    """
    4b (Pasat Internet 4b)
    OpenERP Payment Type App is: pasat4b
    Sale Order Reference:
        - Minimium 4, Maximun 12
    """

    title = _(u'Payment Credit Card Pasat 4b')

    if not 'sale_order' in request.session:
        error = _('Order number is not available. Use navigation menu.')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    conn = connOOOP()
    if not conn:
        error = _('Error when connecting with our ERP. Try again or cantact us.')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    payment_type = conn.ZoookSaleShopPaymentType.filter(app_payment='pasat4b')
    orders = conn.SaleOrder.filter(name=request.session['sale_order'])
        
    if (len(payment_type) > 0) and len(orders) > 0:
        #change payment_type = done
        order = orders[0]
        order.payment_state = 'done'
        order.save()

        pasat4b_dict = {
            "Ds_Merchant_Order": order.name,
            "Ds_Merchant_MerchantCode": PASAT4B_MERCHANT_CODE,
        }

        form = pasat4bPaymentForm(initial=pasat4b_dict)
        debug = DEBUG
        logging.info('Order %s: Pasat 4b form and redirect' % order.name)
        return HttpResponse(render_to_response('pasat4b/form.html', locals(), context_instance=RequestContext(request)))

    else:
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

@login_required
def pasat4b_error(request):
    """
    Error Pasat 4b view
    """

    title = _(u'Error Payment Credit Card Pasat 4b')
    error = _(u'Error return 4b (Pasat Internet 4b) Payment. Go to sale orders and repeat payment')
    return HttpResponse(render_to_response('pasat4b/error.html', {'error':error}, context_instance=RequestContext(request)))

@login_required
def pasat4b_confirm(request):
    """
    Confirmation Pasat 4b view
    """

    if not 'sale_order' in request.session:
        error = _('Order number is not available. Use navigation menu.')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    conn = connOOOP()
    order = request.session['sale_order']

    payment_pasat4b = pasat4bResponse.objects.filter(pszPurchorderNum=order)
    payment = False

    if len(payment_pasat4b) > 0:
        if (payment_pasat4b[0].result == 0): #0 -> transaccin autorizada
            payment = True

    orders = conn.SaleOrder.filter(name=request.session['sale_order'])

    if payment and len(orders) > 0:
        order = orders[0]
        payment_order = conn_webservice('sale.order', 'sale_order_payment', [order.name, 'pasat4b'])

        title = _(u'Confirmation Payment Credit Card Pasat 4b')
        values = {'order':request.session['sale_order'], 'title':title}

        del request.session['sale_order']

        #send email sale order
        SaleOrderEmail(order.id)

        logging.info(_('Order %s: Pasat 4b payment finish') % order.name)

        return HttpResponse(render_to_response('pasat4b/confirm.html', values, context_instance=RequestContext(request)))
    else:
        error = _('Error return 4b (Pasat Internet 4b) Payment. Contact us to check payment')
        return HttpResponse(render_to_response('pasat4b/error.html', {'error':error}, context_instance=RequestContext(request)))

def pasat4b_getorder(request):
    """
    Order Format TXT Pasat 4b
    TODO: Multi Currency
    Get TXT page about order information:
        "M978{{importe}}\n"
        "1\n"
        "1\n"
        "{{order}}\n"
        "1\n"
        "{{importe}}\n"
        "\n"
    """

    conn = connOOOP()
    if not conn:
        error = _('Error when connecting with our ERP. Try again or cantact us.')
        return render_to_response("pasat4b/order_error.html", locals(), context_instance=RequestContext(request))

    order_code = request.GET.get('order') or ''
    payment_type = conn.ZoookSaleShopPaymentType.filter(app_payment='pasat4b')
    orders = conn.SaleOrder.filter(name=order_code)

    if (len(payment_type) > 0) and len(orders) > 0:
        #change payment_type = done
        order = orders[0]
        
        if (order.state == 'draft'):
            amount_total = '%.*f' % (PASAT4B_DECIMAL, order.amount_total)
            amount_total = str(amount_total).replace('.', '') # Replace 123,45 to 12345
            value = "M978%s\n1\n1\n%s\n1\n%s\n\n" % (amount_total, order.name, amount_total)

            logging.info(_('Order %s prossesing Pasat 4b') % order_code)
            logging.info(_('Pasat Values %s') % value.replace('\n', '|'))

            return render_to_response('pasat4b/order.html', {'value': value, })
        else:
            logging.info(_('Error Order %s Pasat 4b') % order_code)
            return render_to_response("pasat4b/order_error.html", locals(), context_instance=RequestContext(request))
    else:
        logging.info(_('Error Order %s Pasat 4b. Not exist') % order_code)
        return render_to_response("pasat4b/order_error.html", locals(), context_instance=RequestContext(request))
