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
            'product_tmpl__metakeyword_'+get_language(): u'%s' % q,
        }
        kwargs_start = {
            'product_tmpl__metakeyword_'+get_language()+'__istartswith': u'%s,' % q,
        }
        kwargs_md = {
            'product_tmpl__metakeyword_'+get_language()+'__icontains': u',%s,' % q,
        }
        kwargs_end = {
            'product_tmpl__metakeyword_'+get_language()+'__iendswith': u',%s' % q,
        }


        product_products = ProductProduct.objects.filter(
                #Q(product_tmpl__status=True), Q(active=True),
                Q(product_tmpl__visibility='all') | Q(product_tmpl__visibility='search') | Q(product_tmpl__visibility='catalog'),
                Q(**kwargs_eq) | Q(**kwargs_start) | Q(**kwargs_md) | Q(**kwargs_end))

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
        title = _(u"'%(tag)s' - Page %(page)s of %(total)s") % {'tag': q, 'page': product_products.number, 'total': num_pages}
        metadescription = _(u"'%(tag)s' - Page %(page)s of %(total)s") % {'tag': q, 'page': product_products.number, 'total': num_pages}
        category_values = {
            'title': title,
            'query': u'“%s”' % q,
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
        return render_to_response("tag/tag.html", category_values, context_instance=RequestContext(request))
    else:
        raise Http404(_('This query is not available because you navigate with bookmarks or search engine. Use navigation menu'))
