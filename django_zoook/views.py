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

from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django_zoook.tools.zoook import siteConfiguration
from django.utils.translation import get_language
from django.db.models import Q
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django_zoook.catalog.models import *
from django_zoook.catalog.views import pathcategory
from django_zoook.settings import *


def doc(request):
    """HomePage Zoook - Developer documentation"""

    site_configuration = siteConfiguration(SITE_ID)
    title = site_configuration.site_title
    metadescription = site_configuration.site_metadescription
    metakeywords = site_configuration.site_metakeywords

    return render_to_response("doc.html", locals(), context_instance=RequestContext(request))


def index(request):
    """All root category products (Featured Products)"""

    site_configuration = siteConfiguration(SITE_ID)
    title = site_configuration.site_title
    metadescription = site_configuration.site_metadescription
    metakeywords = site_configuration.site_metakeywords

    values = []

    categories = ProductCategory.objects.filter(parent=None)

    if len(categories)>0:
        products = ProductTemplate.objects.filter(Q(productproduct__active=True), Q(categ=categories[0]), Q(visibility='all') | Q(visibility='catalog'))

        # get price and base_image product            
        for tplproduct in products:
            prods = ProductProduct.objects.filter(product_tmpl=tplproduct.id)

            prod_images = ProductImages.objects.filter(product=prods[0].id,base_image=True)

            base_image = False
            if len(prod_images) > 0:
                base_image = prod_images[0]

            values.append({'product': tplproduct, 'name': tplproduct.name.lower(), 'product_variant': len(prods), 'price': prods[0].price, 'base_image': base_image})

        # == template values ==
        category_values = {
            'title': title,
            'metadescription': metadescription,
            'metakeywords': metakeywords,
            'values': values,
            'products': products,
            'currency': DEFAULT_CURRENCY,
            'COMPARE_ON': COMPARE_ON
        }
        return render_to_response("index.html", category_values, context_instance=RequestContext(request))
    else:
        raise Http404(_('This category is not available because you navigate with bookmarks or search engine. Use navigation menu'))


""" Custom views """
