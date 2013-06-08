# -*- coding: utf-8 -*-
############################################################################################
#
#    Zoook. OpenERP e-sale, e-commerce Open Source Management Solution
#    Copyright (C) 2011 Zikzakmedia S.L. (<http://www.zikzakmedia.com>). All Rights Reserved
#
#    Module Created: 2013-06-07
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

from django.utils.formats import number_format
from django_zoook.settings import CURRENCY_LABEL_POSITION, DEFAULT_CURRENCY


def money_format(value, decimal_pos=2):
    """
    Format number in money style. Ex 10230.3 -> "$ 10,230.30"
    """
    if value == None:
        value = 0.0
    val = number_format(value, decimal_pos, use_l10n=True, force_grouping=True)
    if CURRENCY_LABEL_POSITION == 'before':
        return DEFAULT_CURRENCY + " " + val
    return val + " " + DEFAULT_CURRENCY
