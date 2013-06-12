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
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django import forms

from transmeta import TransMeta

'''OpenERP Models'''
class ResPartnerTitle(models.Model):
    """Partner Title OpenERP"""
    __metaclass__ = TransMeta

    name = models.CharField(_('name'), max_length=64)
    shortcut = models.CharField(_('shortcut'), max_length=16)
    update_price = models.BooleanField(_('update price'))

    class Meta:
        db_table = 'res_partner_title'
        verbose_name = _('partner title')
        verbose_name_plural = _('partner titles')
        translate = (
            'name',
            'shortcut',
            )

    def __unicode__(self):
        return self.name

class AuthProfile(models.Model):
    """Partner"""
    user = models.ForeignKey(User, verbose_name="User", related_name="user_profile_s", unique=True, null=True, blank=True)
    partner_id = models.IntegerField(null=True, blank=True)

class PartnerForm(forms.Form):
    """Partner Form"""
    name = forms.CharField(max_length=128)
    vat_code = forms.CharField(max_length=2)
    vat = forms.CharField(max_length=32)
    street = forms.CharField(max_length=128)
    zip = forms.CharField(max_length=32)
    city = forms.CharField(max_length=128)
