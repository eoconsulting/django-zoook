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
from django_zoook.blog.models import *
from datetime import datetime
from transmeta import get_real_fieldname_in_each_language

class BlogAdmin(admin.ModelAdmin):

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
    search_fields = get_real_fieldname_in_each_language('name') \
                  + get_real_fieldname_in_each_language('description')
    list_filter = ["status"]
    #prepopulated_fields = {
    #    'slug_en': ('name_en',),
    #    'slug_es': ('name_es',),
    #}

    class Media:
        js = (
            '/static/js/ckeditor/ckeditor.js',
            '/static/js/ckeditor.js',
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

admin.site.register(Blog, BlogAdmin)
