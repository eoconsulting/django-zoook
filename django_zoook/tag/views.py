# -*- coding: utf-8 -*-
############################################################################################
#
#    Zoook. OpenERP e-sale, e-commerce Open Source Management Solution
#    Copyright (C) 2011 Zikzakmedia S.L. (<http://www.zikzakmedia.com>). All Rights Reserved
#
#    Module Created: 03/05/2012
#    Author: Mariano Ruiz <mrsarm@gmail.com>,
#            Enterprise Objects Consulting (<http://www.eoconsulting.com.ar>)
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

from django.shortcuts import render_to_response
from django.http import Http404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils.translation import get_language
from django.db.models import Q

from django_zoook.settings import *

from django_zoook.catalog.models import *
from django_zoook.tools.paginator import *


def keyword(request,tag):
    """All Products filtered by keyword"""

    q = tag
    values = []

    if q:
        kwargs_eq = {
            'metakeyword_'+get_language(): '%s' % q,
        }
        kwargs_start = {
            'metakeyword_'+get_language()+'__istartswith': '%s,' % q,
        }
        kwargs_md = {
            'metakeyword_'+get_language()+'__icontains': ',%s,' % q,
        }
        kwargs_end = {
            'metakeyword_'+get_language()+'__iendswith': ',%s' % q,
        }


        products = ProductTemplate.objects.filter(Q(status=True), Q(product_product_set__active=True),
                                                  Q(visibility='all') | Q(visibility='search') | Q(visibility='catalog'),
                                                  Q(**kwargs_eq) | Q(**kwargs_start) | Q(**kwargs_md) | Q(**kwargs_end))

        # Pagination options
        set_paginator_options(request, 'price')
        total = products.count()
        paginator = Paginator(products, request.session['paginator'])
        num_pages = get_num_pages(products, request.session['paginator'])

        page = int(request.GET.get('page', '1'))

        # If page request (9999) is out of range, deliver last page of results.
        try:
            products = paginator.page(page)
        except (EmptyPage, InvalidPage):
            products = paginator.page(paginator.num_pages)

        # get price and base_image product            
        for tplproduct in products.object_list:
            prods = ProductProduct.objects.filter(product_tmpl=tplproduct.id).order_by('price')

            prod_images = ProductImages.objects.filter(product=prods[0].id,base_image=True)

            base_image = False
            if len(prod_images) > 0:
                base_image = prod_images[0]

            values.append({'product': tplproduct, 'name': tplproduct.name.lower(), 'product_variant': len(prods), 'price': prods[0].price, 'base_image': base_image})

        # == order by name or price ==
        try:
            values.sort(key=lambda x: x[request.session['order']], reverse = request.session['order_by'] == 'desc')
        except:
            pass


        # == template values ==
        title = _(u"'%(tag)s' - Page %(page)s of %(total)s") % {'tag': q, 'page': products.number, 'total': num_pages}
        metadescription = _(u"'%(tag)s' - Page %(page)s of %(total)s") % {'tag': q, 'page': products.number, 'total': num_pages}
        category_values = {
            'title': title,
            'query': u'“%s”' % q,
            'metadescription': metadescription,
            'values': values,
            'products': products,
            'paginator_option': request.session['paginator'],
            'mode_option': request.session['mode'],
            'order_option': request.session['order'],
            'order_by_option': request.session['order_by'],
            'paginator_items': PAGINATOR_ITEMS,
            'catalog_orders': CATALOG_ORDERS,
            'total': total,
            'currency': DEFAULT_CURRENCY,
            'compare_on': COMPARE_ON,
            'update_price': UPDATE_PRICE,
            'currency_position': CURRENCY_LABEL_POSITION,
        }
        return render_to_response("tag/tag.html", category_values, context_instance=RequestContext(request))
    else:
        raise Http404(_('This query is not available because you navigate with bookmarks or search engine. Use navigation menu'))
