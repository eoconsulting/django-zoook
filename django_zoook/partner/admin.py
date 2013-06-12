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

from django.contrib import admin
from django_zoook.partner.models import *
from transmeta import get_real_fieldname_in_each_language

class AuthProfileAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'partner_id',
    )

admin.site.register(AuthProfile, AuthProfileAdmin)

class ResPartnerTitleAdmin(admin.ModelAdmin):

    search_fields = get_real_fieldname_in_each_language('name')

    list_display = (
        'name',
        'shortcut',
        'update_price',
    )

admin.site.register(ResPartnerTitle, ResPartnerTitleAdmin)
