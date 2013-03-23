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


def search(request):
    """All Products filtered by query"""

    q = request.GET.get('q')

    if q:
        kwargs_name = {
            u'product_tmpl__name_'+get_language()+u'__icontains': q,
        }
        kwargs_shortdescription = {
            u'product_tmpl__shortdescription_'+get_language()+u'__icontains': q,
        }
        kwargs_shortdescription = {
            u'variants_'+get_language()+u'__icontains': q,
        }
        product_products = ProductProduct.objects.filter(
                #Q(product_tmpl__status=True), Q(active=True),
                Q(product_tmpl__visibility='all') | Q(product_tmpl__visibility='search') | Q(product_tmpl__visibility='catalog'),
                Q(**kwargs_name) | Q(**kwargs_shortdescription))

        # Pagination options
        set_paginator_options(request, 'price')
        total = product_products.count()
        paginator = Paginator(product_products, request.session['paginator'])
        num_pages = get_num_pages(product_products, request.session['paginator'])
    
        page = int(request.GET.get('page', '1'))
    
        # If page request (9999) is out of range, deliver last page of results.
        try:
            product_products = paginator.page(page)
        except (EmptyPage, InvalidPage):
            product_products = paginator.page(paginator.num_pages)

        # == template values ==
        title = _(u"'%(query)s' - Page %(page)s of %(total)s") % {'query': q, 'page': product_products.number, 'total': product_products.paginator.num_pages}
        metadescription = _(u"'%(query)s' - Page %(page)s of %(total)s") % {'query': q, 'page': product_products.number, 'total': product_products.paginator.num_pages}
        category_values = {
            'title': title,
            'query': u'“%s”' % q,
            'q': q,
            'metadescription': metadescription,
            'product_products': product_products,
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
        return render_to_response("search/search.html", category_values, context_instance=RequestContext(request))
    else:
        raise Http404(_('This query is not available because you navigate with bookmarks or search engine. Use navigation menu'))
