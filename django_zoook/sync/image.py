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
from django_zoook.catalog.models import ProductImages
from django_zoook.tools.conn import conn_webservice

logging.info(_('Sync. Images. Running'))

django_product_images_fields = [field.name for field in ProductImages._meta.fields]

results = conn_webservice('sale.shop', 'dj_export_images', [[OERP_SALE]])

if len(results) == 0:
    logging.info(_('Sync. Images. Not images news or modified'))

for result in results:
    # minicalls with one id (step to step) because it's possible return a big dicctionay and broken memory.
    try:
        values = conn_webservice('base.external.mapping', 'get_oerp_to_external', ['zoook.product.images',[result]])
    except Exception, e:
        logging.error(_('Sync. Images. Error getting image ID %s from OpenERP') % result)
        logging.error('Exception: %s' % e)
        sys.exit(-1)

    logging.debug(values)

    if len(values) > 0:
        img = values[0]

        img_copy = {}
        for k,v in img.iteritems():
            if k in django_product_images_fields or k == 'product_id':
                img_copy[k] = v

        image = ProductImages(**img_copy)
        try:
            image.save()
            logging.info(_('Sync. Images. Image save ID %s') % img['id'])
        except Exception, e:
            logging.error(_('Sync. Images. Error save ID %s') % img['id'])
            logging.error('Exception: %s' % e)
            sys.exit(-1)

logging.info(_('Sync. Images. Done'))

print True
