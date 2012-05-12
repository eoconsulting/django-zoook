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
import time

from config_path import zoook_root
sys.path.append(zoook_root)
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_zoook.settings'

import django_zoook.logconfig

from django_zoook.settings import *
from django.utils.translation import ugettext as _
from django_zoook.catalog.models import ProductCategory
from django_zoook.tools.conn import conn_webservice
from django.core.exceptions import ObjectDoesNotExist

logging.info(_('Sync. Categories. Running'))

results = conn_webservice('sale.shop', 'dj_export_categories', [[OERP_SALE]])
langs = conn_webservice('sale.shop', 'zoook_sale_shop_langs', [[OERP_SALE]])
langs = langs[str(OERP_SALE)]
context = {}

django_product_category_fields = [field.name for field in ProductCategory._meta.fields]

if len(results) == 0:
    logging.info(_('Sync. Categories. Not categories news or modified'))

cat2 = []

for result in results:
    # minicalls with one id (step to step) because it's possible return a big dicctionay and broken memory.
    values = conn_webservice('base.external.mapping', 'get_oerp_to_external', ['zoook.product.category',[result],context,langs])

    logging.debug(str(values))

    if len(values) > 0:
        cat = values[0]

        cat_copy = {}
        for k,v in cat.iteritems():
            if k in django_product_category_fields or k == 'parent_id':
                cat_copy[k] = v

        # create category without parent_id. After, we will create same category with parent_id
        if 'parent_id' in cat_copy:
            if cat_copy['parent_id'] != False:
                cat2.append(cat_copy.copy())
            del cat_copy['parent_id']

        category = ProductCategory(**cat_copy)

        try:
            category.save()

            logging.info(_('Sync. Categories. Category save ID %s') % cat['id'])
        except Exception, e:
            logging.error(_('Sync. Categories. Error save ID %s') % cat['id'])
            logging.error('Exception: %s' % e)
            logging.error(_('Sync. Categories. Fail'))
            sys.exit(-1)

#save category with parent_id value
for cat in cat2:
    try:
        ProductCategory.objects.get(id=cat['parent_id'])  # Check if the parent exist
    except ObjectDoesNotExist:
        logging.warn(_('Sync. Categories. Parent ID %s does not exist. None value assigned') % cat['parent_id'])
    else:
        try:
            category = ProductCategory(**cat)
            category.save()
            logging.info(_('Sync. Categories. Category update ID %s') % cat['id'])
        except Exception, e:
            logging.error(_('Sync. Categories. Error parent_id update ID %s') % cat['id'])
            logging.error('Exception: %s' % e)
            logging.error(_('Sync. Categories. Fail'))
            sys.exit(-1)
        

logging.info(_('Sync. Categories. Done'))

print True
