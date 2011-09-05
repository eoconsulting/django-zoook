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

from settings import *
from tools.conn import conn_webservice
from tools.zoook import checkPartnerID, checkFullName, connOOOP, paginationOOOP
from catalog.models import ProductProduct, ProductTemplate

import datetime
import time
import re

"""Orders. All Orders Partner Available"""
@login_required
def orders(request):
    partner_id = checkPartnerID(request)
    if not partner_id:
        error = _('Are you a customer? Please, contact us. We will create a new role')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))
    full_name = checkFullName(request)
    conn = connOOOP()
    if not conn:
        error = _('Error when connecting with our ERP. Try again or cantact us')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    values = {}
    total = len(conn.SaleOrder.filter(partner_id=partner_id, shop_id=OERP_SALE))
    offset, page_previous, page_next = paginationOOOP(request, total, PAGINATOR_ORDER_TOTAL)

    values = conn.SaleOrder.filter(partner_id=partner_id, shop_id=OERP_SALE, offset=offset, limit=PAGINATOR_ORDER_TOTAL, order='name DESC')

    title = _('All Orders')
    metadescription = _('List all orders of %s') % full_name

    return render_to_response("sale/orders.html", {'title':title, 'metadescription':metadescription, 'values':values, 'page_previous':page_previous, 'page_next':page_next}, context_instance=RequestContext(request))

"""Order. Order Detail Partner"""
@login_required
def order(request, order):
    partner_id = checkPartnerID(request)
    if not partner_id:
        error = _('Are you a customer? Please, contact us. We will create a new role')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))
    full_name = checkFullName(request)
    conn = connOOOP()
    if not conn:
        error = _('Error when connecting with our ERP. Try again or cantact us')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    values = conn.SaleOrder.filter(partner_id=partner_id, name=order, shop_id=OERP_SALE)
    if len(values) == 0:
        error = _('It is not allowed to view this section or not found. Use navigation menu.')
        return render_to_response("user/error.html", locals(), context_instance=RequestContext(request))

    value = values[0]
    title = _('Order %s') % (value.name)
    metadescription = _('Details order %s') % (value.name)

    return render_to_response("sale/order.html", {'title': title, 'metadescription': metadescription, 'value': value}, context_instance=RequestContext(request))

"""Payment. Payment Order"""
@login_required
def payment(request, order):
    partner_id = checkPartnerID(request)
    if not partner_id:
        error = _('Are you a customer? Please, contact us. We will create a new role')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))
    full_name = checkFullName(request)
    conn = connOOOP()
    if not conn:
        error = _('Error when connecting with our ERP. Try again or cantact us')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    values = conn.SaleOrder.filter(partner_id=partner_id, name=order, shop_id=OERP_SALE)
    if len(values) == 0:
        error = _('It is not allowed to view this section or not found. Use navigation menu.')
        return render_to_response("user/error.html", locals(), context_instance=RequestContext(request))

    value = values[0]

    if value.state != 'draft':
        error = _('Your order is in progress. Contact with us')
        return render_to_response("user/error.html", locals(), context_instance=RequestContext(request))

    sale_shop = conn.SaleShop.filter(id=OERP_SALE)[0]
    payments = sale_shop.zoook_payment_types
    
    title = _('Payment Order %s') % (value.name)
    metadescription = _('Payment Order %s') % (value.name)

    return render_to_response("sale/payment.html", {'title': title, 'metadescription': metadescription, 'value': value, 'payments': payments}, context_instance=RequestContext(request))

"""Check Order"""
def check_Order(conn, partner_id, OERP_SALE):
    orders = conn.SaleOrder.filter(partner_id=partner_id, state='draft', payment_state ='draft', shop_id=OERP_SALE)

    # get a draft order
    if len(orders)>0:
        order = orders[0]
    # new order
    else:
        partner = conn.ResPartner.get(partner_id)
        partner_addresses = conn.ResPartnerAddress.filter(partner_id=partner_id)
        address = {}
        for partner_address in partner_addresses:
            if partner_address.type == 'delivery':
                address['delivery'] = partner_address
            if partner_address.type == 'invoice':
                address['invoice'] = partner_address
            if partner_address.type == 'contact':
                address['contact'] = partner_address
       
        if len(address) > 0:
            if not 'delivery' in address:
                address['delivery'] = partner_addresses[0]
            if not 'invoice' in address:
                address['invoice'] = partner_addresses[0]
            if not 'contact' in address:
                address['contact'] = partner_addresses[0]
            
            #create new order
            shop = conn.SaleShop.get(OERP_SALE)
            order = conn.SaleOrder.new()
            order.shop_id = shop
            order.date_order = datetime.date.today() # not time.strftime('%Y-%m-%d')
            order.partner_id = partner
            order.partner_invoice_id = address['invoice']
            order.partner_order_id = address['contact']
            order.partner_shipping_id = address['delivery']
            order.picking_policy = 'one'
            order.pricelist_id = partner.property_product_pricelist
            order.save()
        else:
            order = 'error'

    return order

"""Check Product"""
def check_product(conn, code):
    #check if this product exist
    product = False
    products = ProductProduct.objects.filter(code=code)
    if len(products)> 0:
        product = products[0]

    return product

"""Checkout. Order cart"""
@login_required
def checkout(request):
    if 'sale_order' in request.session:
        return HttpResponseRedirect("/sale/order/%s" % request.session['sale_order'])

    message = False
    partner_id = checkPartnerID(request)
    if not partner_id:
        error = _('Are you a customer? Please, contact us. We will create a new role')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))
    full_name = checkFullName(request)
    conn = connOOOP()
    if not conn:
        error = _('Error when connecting with our ERP. Try again or cantact us')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    order = check_Order(conn, partner_id, OERP_SALE)
    
    if order == 'error':
        return HttpResponseRedirect("/partner/partner/")

    if request.method == 'POST':
        qty = int(request.POST['qty'])
        code = request.POST['code']
        #check product is available to add to cart
        product = check_product(conn, code)
        if product:
            #check if this product exist
            product_line = conn.SaleOrderLine.filter(order_id=order.id, product_id=product.id)
            product = conn.ProductProduct.get(product.id)
            partner = conn.ResPartner.get(partner_id)

            if len(product_line) > 0: #product line exist -> update
                order_line = conn.SaleOrderLine.get(product_line[0].id)
                order_line.product_uom_qty = qty+product_line[0].product_uom_qty
                order_line.save()
            else: #product line not exist -> create
                values = [
                    [order.id], #ids
                    partner.property_product_pricelist.id, #pricelist
                    product.id, #product
                    qty, #qty
                    False, #uom
                    0, #qty_uos
                    False, #uos
                    '', #name
                    partner_id, #partner_id
                ]
                product_id_change = conn_webservice('sale.order.line','product_id_change', values)

                if not product_id_change['warning']:
                    product_value = product_id_change['value']
                    order_line = conn.SaleOrderLine.new()
                    order_line.order_id = order
                    order_line.name = product_id_change['value']['name']
                    if 'notes' in product_value:
                        order_line.notes = product_id_change['value']['notes']
                    order_line.product_id = product
                    order_line.product_uom_qty = qty
                    order_line.product_uom = product.product_tmpl_id.uom_id
                    order_line.delay = product_id_change['value']['delay']
                    order_line.th_weight = product_id_change['value']['th_weight']
                    order_line.type = product_id_change['value']['type']
                    order_line.price_unit = product_id_change['value']['price_unit']
                    order_line.tax_id = [conn.AccountTax.get(t_id) for t_id in product_id_change['value']['tax_id']]
                    order_line.product_packaging = ''
                    order_line.save()
                else:
                    message = product_id_change['warning']
                    
            #recalcule order (refresh amount)
            order = check_Order(conn, partner_id, OERP_SALE)

    #list order lines
    lines = conn.SaleOrderLine.filter(order_id=order.id)

    title = _('Checkout')
    metadescription = _('Checkout order %s') % (SITE_TITLE)
    
    values = {
        'title': title,
        'metadescription': metadescription,
        'message':message,
        'order':order,
        'lines': lines,
    }
    
    #delivery
    if len(lines)>0:
        values['deliveries'] = conn_webservice('sale.order','delivery_cost', [order.id])
        #Address invoice/delivery
        values['address_invoices'] = conn.ResPartnerAddress.filter(partner_id=partner_id,type='invoice')
        values['address_deliveries'] = conn.ResPartnerAddress.filter(partner_id=partner_id,type='delivery')
        sale_shop = conn.SaleShop.filter(id=OERP_SALE)[0]
        values['payments'] = sale_shop.zoook_payment_types

    return render_to_response("sale/checkout.html", values, context_instance=RequestContext(request))

"""Checkout. Order cart"""
@login_required
def checkout_remove(request, code):
    products = ProductProduct.objects.filter(code=code)
    if len(products) > 0:
        partner_id = checkPartnerID(request)
        if not partner_id:
            error = _('Are you a customer? Please, contact us. We will create a new role')
            return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))
        full_name = checkFullName(request)
        conn = connOOOP()
        if not conn:
            error = _('Error when connecting with our ERP. Try again or cantact us')
            return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))
        order = check_Order(conn, partner_id, OERP_SALE)
        order_lines = conn.SaleOrderLine.filter(order.id, product_id=products[0].id)
        if len(order_lines) > 0:
            order_line = conn.SaleOrderLine.get(order_lines[0].id)
            order_line.delete()

    return HttpResponseRedirect("/sale/checkout/")

"""Checkout. Confirm"""
@login_required
def checkout_confirm(request):
    if 'sale_order' in request.session:
        return HttpResponseRedirect("/sale/order/%s" % request.session['sale_order'])

    if request.method == 'POST':
        partner_id = checkPartnerID(request)
        if not partner_id:
            error = _('Are you a customer? Please, contact us. We will create a new role')
            return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))
        full_name = checkFullName(request)
        conn = connOOOP()
        if not conn:
            error = _('Error when connecting with our ERP. Try again or cantact us')
            return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))
            
        partner = conn.ResPartner.get(partner_id)
        order = check_Order(conn, partner_id, OERP_SALE)

        if order.state != 'draft':
            return HttpResponseRedirect("/sale/")

        delivery = request.POST['delivery']
        payment = request.POST['payment']
        address_invoice = int(request.POST['address_invoice'])
        address_delivery = int(request.POST['address_delivery'])

        #delivery
        delivery = delivery.split('|')
        carrier = conn.DeliveryCarrier.filter(code=delivery[0])
        if len(carrier) == 0:
            return HttpResponseRedirect("/sale/checkout/")
        carrier = carrier[0]

        values = [
            [order.id], #ids
            partner.property_product_pricelist.id, #pricelist
            carrier.product_id.id, #product
            1, #qty
            False, #uom
            0, #qty_uos
            False, #uos
            '', #name
            partner.id, #partner_id
        ]

        product_id_change = conn_webservice('sale.order.line','product_id_change', values)
        order_line = conn.SaleOrderLine.new()
        order_line.order_id = order
        order_line.name = carrier.product_id.name
        order_line.product_id = carrier.product_id
        order_line.product_uom_qty = 1
        order_line.product_uom = carrier.product_id.product_tmpl_id.uom_id
        order_line.delay = product_id_change['value']['delay']
        order_line.th_weight = product_id_change['value']['th_weight']
        order_line.type = product_id_change['value']['type']
        order_line.price_unit = float(re.sub(',','.',delivery[1]))
        order_line.tax_id = [conn.AccountTax.get(t_id) for t_id in product_id_change['value']['tax_id']]
        order_line.product_packaging = ''
        order_line.save()

        #delivery
        order.carrier_id = carrier

        #payment type
        payment_type = conn.ZoookSaleShopPaymentType.filter(app_payment=payment)
        if len(payment_type) > 0:
            order.payment_type = payment_type[0].payment_type_id
            order.picking_policy = payment_type[0].picking_policy
            order.order_policy = payment_type[0].order_policy
            order.invoice_quantity = payment_type[0].invoice_quantity

        #Replace invoice address and delivery address
        if address_invoice:
            address_invoice = conn.ResPartnerAddress.get(address_invoice)
            if address_invoice:
                order.partner_invoice_id = address_invoice
        if address_delivery:
            address_delivery = conn.ResPartnerAddress.get(address_delivery)
            if address_delivery:
                order.partner_shipping_id = address_delivery

        #payment state
        order.payment_state = 'checking'
        order.save()

        request.session['sale_order'] = order.name

        return HttpResponseRedirect("/payment/%s/" % payment_type[0].app_payment)
    else:
        return HttpResponseRedirect("/sale/checkout/")

