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

from django.db import models

from sermepa.sermepa.signals import payment_was_successful, payment_was_error, signature_error

#signals
def payment_ok(sender, **kwargs):
    pass

def payment_ko(sender, **kwargs):
    pass

def sermepa_ipn_error(sender, **kwargs):
    pass

payment_was_successful.connect(payment_ok)
payment_was_error.connect(payment_ko)
signature_error.connect(sermepa_ipn_error)
