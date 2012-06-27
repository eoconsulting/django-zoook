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

from django_zoook.settings import *
from django_zoook.tools.conn import conn_webservice
from django_zoook.tools.zoook import connOOOP

from django_zoook.sale.email import SaleOrderEmail

import time
import logging

@login_required
def index(request):
    """
    Debit Bank View
    """

    title = _(u'Payment Debit Bank. Add Bank Number')

    if not 'sale_order' in request.session:
        error = _('Order number is not available. Use navigation menu.')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))
        
    values = {'order':request.session['sale_order']}

    return render_to_response("debit/bank.html", values, context_instance=RequestContext(request))
        
@login_required
def confirm(request):
    """
    Debit
    OpenERP Payment Type App is: debit
    """

    title = _(u'Payment Debit Bank')
    context_instance=RequestContext(request)

    if not 'sale_order' in request.session:
        error = _('Order number is not available. Use navigation menu.')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    conn = connOOOP()
    if not conn:
        error = _('Error when connecting with our ERP. Try again or cantact us.')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    payment_type = conn.ZoookSaleShopPaymentType.filter(app_payment='debit')
    orders = conn.SaleOrder.filter(name=request.session['sale_order'])
    
    bank_number = request.POST.get('number', '')

    if not bank_number:
        return HttpResponseRedirect("%s/sale/checkout/" % (context_instance['LOCALE_URI']))

    if (len(payment_type) > 0) and len(orders) > 0:
        order = orders[0]
        partner_banks = conn.ResPartnerBank.filter(acc_number=bank_number,partner_id=order.partner_id.id)

        #add bank number res_partner_bank
        if not len(partner_banks)>0:
            country_id = order.partner_invoice_id.country_id.id
            bank_code = bank_number[:4]
            banks = conn.ResBank.filter(country=country_id,code=bank_code)

            # not bank available
            if not len(banks)>0:
                banks = conn.ResBank.all() #get first bank available. TODO: get on_change/country

            try:
                res_partner_bank = conn.ResPartnerBank.new()
                res_partner_bank.acc_number = str(bank_number)
                res_partner_bank.partner_id = order.partner_id
                res_partner_bank.bank = banks[0]
                res_partner_bank.state = 'bank'
                res_partner_bank.default_bank = 0
                res_partner_bank.country_id = ''
                res_partner_bank.state_id = ''
                res_partner_bank.save()
            except:
                logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), 'Bank Partner error: %s' % (bank_number)))

        #change payment_type = done
        order.payment_state = 'done'
        order.save()

        payment_order = conn_webservice('sale.order', 'sale_order_payment', [order.name, 'debit'])

        values = {'order':request.session['sale_order'],'payment_type':payment_type[0]}
        del request.session['sale_order']

        #send email sale order
        SaleOrderEmail(order.id)

        logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), 'Order %s: debit payment finish' % (order.name) ))
        return render_to_response("debit/confirm.html", values, context_instance=RequestContext(request))
    else:
        error = _('Error payment this order or is null. Contact Us or use navigation menu')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))
