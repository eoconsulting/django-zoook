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
from content.models import *
from datetime import datetime

class ContentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,   {'fields': ['name','slug']}),
        ('Description', {'fields': ['description_en','description_es','description_ca']}),
        ('SEO', {'fields': ['metadesc_en','metadesc_es','metadesc_ca','metakey_en','metakey_es','metakey_ca']}),
        ('Page', {'fields': ['status','sort_order','template']}),
    ]
    list_display = (
        'name',
        'slug',
        'sort_order',
        'created_by',
        'created_on',
        'updated_by',
        'updated_on',
        'status'
    )
    search_fields = ["name", "description"]
    list_filter = ["status"]
    prepopulated_fields = {'slug': ('name',)}

    class Media:
        js = (
            'js/ckeditor/ckeditor.js',
            'js/ckeditor.js',
        )

    def save_model(self, request, obj, form, change): 
        """
        Overrided because I want to also set who created this instance.
        """
        instance = form.save(commit=False)
        if instance.id is None:
            new = True
            instance.created_by = request.user
        instance.updated_by = request.user
        instance.save()
        return instance

admin.site.register(Content, ContentAdmin)
