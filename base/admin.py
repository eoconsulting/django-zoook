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

from django.contrib import admin

from base.models import *

class ResCountryAdmin(admin.ModelAdmin):

    search_fields = ["name"]

    list_display = (
        'name',
        'code',
        'status',
    )

admin.site.register(ResCountry, ResCountryAdmin)

class ResCountryStateAdmin(admin.ModelAdmin):

    search_fields = ["name"]

    list_display = (
        'name',
        'code',
        'country',
    )

admin.site.register(ResCountryState, ResCountryStateAdmin)
