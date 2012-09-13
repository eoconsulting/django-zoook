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

from django.utils.translation import ugettext as _
from django.utils.translation import get_language
from django.core.mail import EmailMessage
import logging

from django_zoook.settings import *
from django_zoook.tools.conn import conn_webservice
from django_zoook.tools.zoook import connOOOP

def SaleOrderEmail(order):
    """
    Send email Order
    order Int (ID)
    Return True/False
    """

    conn = connOOOP()
    shop = conn.SaleShop.get(OERP_SALE)

    context = {}
    context['active_id'] = shop.email_sale_order.id
    values = [
        [], #ids
        order, #rel_model_ref
        context, #context
    ]
    body_template = conn_webservice('poweremail.preview','on_change_ref', values)

    customer_email = body_template['value']['to']
    bcc=None
    if body_template['value']['bcc'] and body_template['value']['bcc'] != 'False':
        bcc = [body_template['value']['bcc']]
    
    if customer_email != 'False':
        subject = body_template['value']['subject']
        if body_template['value']['body_html']:
            body = body_template['value']['body_html']
        else:
            body = body_template['value']['body_text']
        email = EmailMessage(subject, body, EMAIL_FROM, to=[customer_email], bcc=bcc, headers = {'Reply-To': EMAIL_REPPLY})
        if body_template['value']['body_html']:
            email.content_subtype = "html"

        try:
            email.send()
            return None
        except Exception, e:
            logging.warn('SaleOrderEmail: Order ID %s - Error sending email: %s' % (order, str(e)))
            error = _("Your order is in process but we don't send email. Check in your order customer section.")
            return error
