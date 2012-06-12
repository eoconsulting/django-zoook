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
from django_zoook.base.models import ResCountry, ResCountryState
from django_zoook.tools.conn import conn_webservice

logging.info(_('Sync. Configuration. Running'))

langs = conn_webservice('sale.shop', 'zoook_sale_shop_langs', [[OERP_SALE]])
langs = langs[str(OERP_SALE)]
context = {}

"""
countries / states
"""
results = conn_webservice('sale.shop', 'dj_export_countries', [[OERP_SALE]])

for result in results:
    # minicalls with one id (step to step) because it's possible return a big dicctionay and broken memory.
    values = conn_webservice('base.external.mapping', 'get_oerp_to_external', ['zoook.res.country',[result],context,langs])

    logging.debug(str(values))

    if len(values) > 0:
        count = values[0]
        country = ResCountry(**count)

        try:
            country.save()
            states = conn_webservice('sale.shop', 'dj_export_states', [count['id']])

            for state in states:
                stats = conn_webservice('base.external.mapping', 'get_oerp_to_external', ['zoook.res.country.state', [state],context,langs])
                if len(stats) > 0:
                    stat = stats[0]
                    state_country = ResCountryState(**stat)
                    try:
                        state_country.save()
                    except Exception, e:
                        logging.error(_('Sync. Configuration State. Error save ID %s\nException: %s') % (stat['id'], str(e)))
                        sys.exit(-1)

            logging.info(_('Sync. Configuration. Country save ID %s') % count['id'])
        except Exception, e:
            logging.error(_('Sync. Configuration Country. Error save ID %s\nException: %s') % (count['id'], str(e)))
            sys.exit(-1)

logging.info(_('Sync. Configuration. Done'))


print True
