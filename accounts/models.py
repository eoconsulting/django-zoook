# -*- encoding: utf-8 -*-
############################################################################################
#
#    Zoook e-sale for OpenERP, Open Source Management Solution	
#    Copyright (C) 2011 Zikzakmedia S.L. (<http://www.zikzakmedia.com>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
############################################################################################

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django import forms

class Partner(models.Model):
    """Partner"""
    user = models.ForeignKey(User, unique=True)
    partner_id = models.IntegerField(unique=True)
#    address_id = models.IntegerField(unique=True)

    class Meta:
        verbose_name = _('partner')
        verbose_name_plural = _('partners')

    def __unicode__(self):
        return self.user.username

class PartnerForm(forms.Form):
    """Partner Form"""
    name = forms.CharField(max_length=128)
    vat_code = forms.CharField(max_length=2)
    vat = forms.CharField(max_length=32)

#    addr_name = forms.CharField(max_length=64)
#    addr_street = forms.CharField(max_length=128)
#    addr_zip = forms.CharField(max_length=24)
#    addr_city = forms.CharField(max_length=128)
#    addr_country_id = forms.CharField()
#    addr_email = forms.EmailField(max_length=240)
#    addr_phone = forms.CharField(max_length=64)
