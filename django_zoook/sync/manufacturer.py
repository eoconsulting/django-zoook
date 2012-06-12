#!/usr/bin/env python
# -*- encoding: utf-8 -*-
############################################################################################
#
#    Zoook. OpenERP e-sale, e-commerce Open Source Management Solution
#    Copyright (C) 2012 Zikzakmedia S.L. (<http://www.zikzakmedia.com>). All Rights Reserved
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
from django.template import defaultfilters
from django_zoook.catalog.models import ResManufacturer
from django_zoook.tools.zoook import connOOOP

logging.info(_('Sync. Manufacturers. Running'))

"""
manufacturers
"""
conn = connOOOP()
if not conn:
    logging.error(_('Error connecting to ERP'))

for result in conn.ResPartner.filter(manufacturer=True):
    values = {
        'id': result.id,
        'name': result.name,
        'slug': defaultfilters.slugify(result.name),
    }

    manufacturer = ResManufacturer(**values)
    try:
        manufacturer.save()            
        logging.info(_('Sync. Manufacturers save ID %s') % result.id)
    except:
        logging.error(_('Sync. Manufacturers. Error save ID %s') % result.id)

logging.info(_('Sync. Manufacturers. Done'))

print True
