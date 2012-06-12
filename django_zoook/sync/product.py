#!/usr/bin/env python
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

import os
import sys
import logging

from config_path import zoook_root
sys.path.insert(0, zoook_root)
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_zoook.settings'

import django_zoook.logconfig

from django_zoook.settings import *
from django.utils.translation import ugettext as _
from django_zoook.catalog.models import ProductProduct, ProductTemplate, ResManufacturer
from django_zoook.tools.conn import conn_webservice

logging.info(_('Sync. Products. Running'))

"""
for product.template
    for product.product
        if product.attributes
"""

results = conn_webservice('sale.shop', 'dj_export_products', [[OERP_SALE]])
langs = conn_webservice('sale.shop', 'zoook_sale_shop_langs', [[OERP_SALE]])
langs = langs[str(OERP_SALE)]
context = {}

django_product_template_fields = [field.name for field in ProductTemplate._meta.fields]
django_product_product_fields = [field.name for field in ProductProduct._meta.fields]

if len(results) == 0:
    logging.info(_('Sync. Products Template. Not products template news or modified'))

for result in results:
    # minicalls with one id (step to step) because it's possible return a big dicctionay and broken memory.
    try:
        values = conn_webservice('base.external.mapping', 'get_oerp_to_external', ['zoook.product.template',[result['product_template']],context,langs])
    except Exception, e:
        logging.error(_('Sync. Products Template. Error getting template ID %s from OpenERP') % result['product_template'])
        logging.error('Exception: %s' % e)
        sys.exit(-1)

    logging.debug(values)

    if len(values) > 0:
        product_template = values[0]

        #detect m2m fiels (is a list) and add values
        prod_template = {}
        m2m_template = {}
        for k,v in product_template.iteritems():
            if type(v).__name__=='list':
                m2m_template[k] = v
            else:
                if k in django_product_template_fields:
                    prod_template[k] = v
        
        # add manufacturer if available
        if 'manufacturer' in prod_template:
            manufacturer = prod_template['manufacturer']
            del prod_template['manufacturer']
            res_manufacturer = ResManufacturer.objects.filter(id=manufacturer)
            if res_manufacturer:
                prod_template['manufacturer'] = res_manufacturer[0]

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
                #for prod_id in v:
                #check if this product.template exists
                #    prodtmp = ProductTemplate.objects.filter(id=prod_id)
                #    if not prodtmp:
                #        logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), _('Sync. Products Template. Product Template NOT exist ID %s') % prod_id))
                #        v.remove(prod_id)

                getattr(prod_template, k).clear()
                getattr(prod_template, k).add(*v) #TODO: m2m fields deleted (not create all fields)
                prod_template.save()
                #~ prod_template.save_m2m()

            logging.info(_('Sync. Products Template. Product Template save ID %s') % product_template['id'])
        except Exception, e:
            logging.error(_('Sync. Products Template. Error save ID %s') % product_template['id'])
            logging.error('Exception: %s' % e)
    
        for prod in result['product_product']:
            logging.debug(_('Sync. Products Product. Get ID %s') % prod)

            # minicalls with one id (step to step) because it's possible return a big dicctionay and broken memory.
            context = {'shop':OERP_SALE, 'product_id': prod}
            values = conn_webservice('base.external.mapping', 'get_oerp_to_external', ['zoook.product.product',[prod],context,langs])

            logging.debug(values)

            if len(values) > 0:
                product = values[0]
                product_copy = {}
                for k,v in product.iteritems():
                    if k in django_product_product_fields or k == 'product_tmpl_id':
                        product_copy[k] = v

                prod = ProductProduct(**product_copy)
                try:
                    prod.save()
                    logging.info(_('Sync. Products. Product save ID %s') % product['id'])
                except Exception, e:
                    logging.error(_('Sync. Products. Error save ID %s') % product['id'])
                    logging.error('Exception: %s' % e)
                    sys.exit(-1)

logging.info(_('Sync. Products. Done'))

print True
