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
from django.utils.translation import get_language, ugettext as _
from django_zoook.tools.zoook import siteConfiguration
from django_zoook.catalog.models import *
from django_zoook.settings import *
from django.db.models import Q


def doc(request):
    """HomePage Zoook - Developer documentation"""

    title = _(u'Zoook. OpenERP e-sale')
    return render_to_response("doc.html", locals(), context_instance=RequestContext(request))


def index(request):
    """All root category products (Featured Products)"""

    site_configuration = siteConfiguration(SITE_ID)
    title = site_configuration.site_title
    metadescription = site_configuration.site_metadescription
    metakeywords = site_configuration.site_metakeywords

    values = []

    categories = ProductCategory.objects.filter(parent=None)
    root_category = categories[0]

    if len(categories)>0:
        products = ProductTemplate.objects.filter(
                            Q(product_product_set__active=True),
                            Q(categ=root_category),
                            Q(visibility='all') | Q(visibility='catalog')
                        ).distinct()

        # get price and base_image product            
        for tplproduct in products:
            prods = ProductProduct.objects.filter(product_tmpl=tplproduct.id)

            i = 0
            prod_images = []
            while i<len(prods) and len(prod_images)==0: 
                prod_images = ProductImages.objects.filter(product=prods[i].id,base_image=True)
                i+=1

            base_image = False
            if len(prod_images) > 0:
                base_image = prod_images[0]

            values.append({'product': tplproduct, 'name': tplproduct.name.lower(), 'product_variant': len(prods), 'prods': prods, 'base_image': base_image})

        # == template values ==
        category_values = {
            'title': title,
            'metadescription': metadescription,
            'metakeywords': metakeywords,
            'values': values,
            'products': products,
            'currency': DEFAULT_CURRENCY,
            'currency_position': CURRENCY_LABEL_POSITION,
            'compare_on': COMPARE_ON,
            'category_decription': root_category.description if root_category.description != 'False' else None,
            'update_price': UPDATE_PRICE,
        }
        return render_to_response("index.html", category_values, context_instance=RequestContext(request))
    else:
        raise Http404(_('This category is not available because you navigate with bookmarks or search engine. Use navigation menu'))


""" Custom views """
