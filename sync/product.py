#!/usr/bin/env python
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

import os
import sys
import logging
import time

from config_path import djpath
sys.path.append(djpath)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from settings import *
from django.utils.translation import ugettext as _
from catalog.models import ProductProduct, ProductTemplate, ProductManufacturerAttribute
from tools.conn import conn_webservice

logging.basicConfig(filename=LOGFILE,level=logging.INFO)
logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), _('Sync. Products. Running')))

"""
Product Template
"""
results = conn_webservice('sale.shop', 'dj_export_products_template', [[OERP_SALE]])

if len(results) == 0:
    logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), _('Sync. Products Template. Not products template news or modified')))

for result in results:
    # minicalls with one id (step to step) because it's possible return a big dicctionay and broken memory.
    values = conn_webservice('base.external.mapping', 'get_oerp_to_external', ['zoook.product.template',[result]])

    if DEBUG:
        logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), values))

    if len(values) > 0:
        product_template = values[0]

        #detect m2m fiels (is a list) and add values
        prod_template = {}
        m2m_template = {}
        for k,v in product_template.iteritems():
            if type(v).__name__=='list':
                m2m_template[k] = v
            else:
                prod_template[k] = v

        prod_template = ProductTemplate(**prod_template)

        # m2m fields
        #ptemplate = ProductTemplate(id=1,name_es='OpenERP Service')
        ##ptemplate.categ.clear()
        #ptemplate.categ.remove(8)
        #ptemplate.categ.add(3,6)
        #ptemplate.save()

        try:
            prod_template.save()
            for k,v in m2m_template.iteritems():
                getattr(prod_template, k).clear()
                getattr(prod_template, k).add(*v) #TODO: m2m fields deleted (not create all fields)
            prod_template.save_m2m()

            logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), _('Sync. Products Template. Product Template save ID %s') % product_template['id']))
        except:
            logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), _('Sync. Products Template. Error save ID %s') % product_template['id']))

logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), _('Sync. Products Template. Done')))

"""
Product Product
"""
results = conn_webservice('sale.shop', 'dj_export_products', [[OERP_SALE]])

if len(results) == 0:
    logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), _('Sync. Products. Not products news or modified')))

for result in results:
    # minicalls with one id (step to step) because it's possible return a big dicctionay and broken memory.
    context = {'shop':OERP_SALE, 'product_id': result}
    values = conn_webservice('base.external.mapping', 'get_oerp_to_external', ['zoook.product.product',[result], context])

    if DEBUG:
        logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), values))

    if len(values) > 0:
        product = values[0]
        prod = ProductProduct(**product)
        try:
            prod.save()
            logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), _('Sync. Products. Product save ID %s') % product['id']))

            #product attribute
            attributes = conn_webservice('sale.shop', 'dj_export_products_attribute', [product['id'], OERP_SALE])
            if len(attributes) > 0:
                values = conn_webservice('base.external.mapping', 'get_oerp_to_external', ['zoook.product.manufacturer.attribute', attributes])
                for attributes in values:
                    prod_attributes = ProductManufacturerAttribute(**attributes)
                    try:
                        prod_attributes.save()
                    except:
                        logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), _('Sync. Products Attribute. Error save ID %s') % product['id']))

                if DEBUG:
                    logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), values))
        except:
            logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), _('Sync. Products. Error save ID %s') % product['id']))

logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), _('Sync. Products. Done')))

print True
