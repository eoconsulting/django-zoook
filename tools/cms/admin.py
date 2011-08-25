# -*- encoding: utf-8 -*-
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

from tools.cms.models import *

"""
Menus Admin
"""
class MenuAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'slug',
        'base_url'
    )
    search_fields = ["name", "base_url"]
    prepopulated_fields = {
        'slug': ('name',),
    }

admin.site.register(Menu,MenuAdmin)

class MenuItemAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'menu',
        'order',
        'link_url'
    )
    search_fields = ["title", "menu","link_url"]
    list_filter = ["login_required"]

admin.site.register(MenuItem,MenuItemAdmin)

"""
Modules Admin
"""
class ModulesAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'position',
        'status'
    )

    class Media:
        js = (
            'js/ckeditor/ckeditor.js',
            'js/ckeditor.js',
        )

admin.site.register(Modules,ModulesAdmin)
