# -*- coding: utf-8 -*-
############################################################################################
#
#    Zoook. OpenERP e-sale, e-commerce Open Source Management Solution
#
#    Module Created: 2012-09-28
#    Author: Mariano Ruiz <mrsarm@gmail.com>,
#            Enterprise Objects Consulting (<http://www.eoconsulting.com.ar>)
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
    Bank Transfer
    OpenERP Payment Type App is: banktransfer
    """

    title = _('Payment Bank Transfer')

    if not 'sale_order' in request.session:
        error = _('Order number is not available. Use navigation menu.')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    conn = connOOOP()
    if not conn:
        error = _('Error when connecting with our ERP. Try again or cantact us.')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    payment_type = conn.ZoookSaleShopPaymentType.filter(app_payment='banktransfer')
    orders = conn.SaleOrder.filter(name=request.session['sale_order'])
        
    if (len(payment_type) > 0) and len(orders) > 0:
        #change payment_type = done
        order = orders[0]
        order.payment_state = 'done'
        order.save()

        payment_order = conn_webservice('sale.order', 'sale_order_payment', [order.name, 'check'])

        values = {'order':request.session['sale_order'],'payment_type':payment_type[0]}
        del request.session['sale_order']

        #send email sale order
        mailresult = SaleOrderEmail(order.id)
        if mailresult:
            values['error'] = mailresult
        
        logging.info('Order %s: check payment finish' % order.name)
        return render_to_response("banktransfer/banktransfer.html", values, context_instance=RequestContext(request))
    else:
        error = _('Error payment this order or is null. Contact Us or use navigation menu')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))
