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
from catalog.models import *
from datetime import datetime

class ProductCategoryAdmin(admin.ModelAdmin):

    list_display = (
        'name',
    )
    search_fields = ["name"]
    extra = 0
#    list_filter = ["status"]

admin.site.register(ProductCategory, ProductCategoryAdmin)

class ProductTemplateAdmin(admin.ModelAdmin):

    list_display = (
        'name_en',
    )
    search_fields = ["name"]
    extra = 0
#    list_filter = ["status"]

admin.site.register(ProductTemplate, ProductTemplateAdmin)

class ProductProductAdmin(admin.ModelAdmin):

    list_display = (
        'code',
        'product_tmpl',
    )
    search_fields = ["product_tmpl"]
    extra = 0
#    list_filter = ["status"]

admin.site.register(ProductProduct, ProductProductAdmin)

class ProductManufacturerAttributeAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'product',
    )
    search_fields = ["product"]
    extra = 0
#    list_filter = ["status"]

admin.site.register(ProductManufacturerAttribute, ProductManufacturerAttributeAdmin)

class ProductImagesAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'product',
    )
    search_fields = ["product"]
    extra = 0
#    list_filter = ["status"]

admin.site.register(ProductImages, ProductImagesAdmin)
