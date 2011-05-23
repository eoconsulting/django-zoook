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

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils.translation import get_language
from django.db.models import Q

from settings import *

from catalog.models import *

"""Category Children"""
def collect_children(category, level=0, children=None):
    if children is None:
        children = []

    values = ProductCategory.objects.filter(parent=category).order_by('sequence')

    for i, child in enumerate(values):
        children.append((child.id, level))
        collect_children(child, level+1, children)

    return children

def index(request):
    """Index Catalog. All Categories list"""
    root_category = ProductCategory.objects.filter(parent=None)

    values = []
    if len(root_category) > 0:
        categories = collect_children(root_category[0].id, 1, None)

        oldlevel = 0
        for (category, level) in categories:
            values.append((ProductCategory.objects.get(id=category), level, oldlevel))
            oldlevel = level

    title = _('Categories')
    metadescription = _('List all categories of %s') % SITE_TITLE
    return render_to_response("catalog/index.html", {'title': title, 'metadescription': metadescription, 'values': values}, context_instance=RequestContext(request))


def category(request,category):
    """All Questions filtered by category"""
    values = []

    if category:
        kwargs = {
            'slug_'+get_language(): category, #slug is unique
            'status': True,
        }
        categories = ProductCategory.objects.filter(**kwargs)

        if len(categories)>0:
            products = ProductTemplate.objects.filter(Q(productproduct__active=True), Q(categ=categories[0]), Q(visibility='all') | Q(visibility='catalog'))

            # == Session Catalog ==
            # paginator options = session
            request.session['paginator'] = request.GET.get('paginator') and int(request.GET.get('paginator')) or  request.session['paginator'] or PAGINATOR_TOTAL

            # mode options = session
            request.session['mode'] = request.GET.get('mode') and request.GET.get('mode') or request.session['mode'] or 'grid'

            # order options = session
            request.session['order'] = request.GET.get('order') and request.GET.get('order') or request.session['order'] or 'price'

            # order_by options = session
            request.session['order_by'] = request.GET.get('order_by') and request.GET.get('order_by') or request.session['order_by'] or 'asc'

            # == pagination ==
            total = len(products)
            paginator = Paginator(products, request.session['paginator'])

            try:
                page = int(request.GET.get('page', '1'))
            except ValueError:
                page = 1

            # If page request (9999) is out of range, deliver last page of results.
            try:
                products = paginator.page(page)
            except (EmptyPage, InvalidPage):
                products = paginator.page(paginator.num_pages)

            # get price and base_image product            
            for tplproduct in products.object_list:
                prods = ProductProduct.objects.filter(product_tmpl=tplproduct.id).order_by('price')

                prod_images = ProductImages.objects.filter(product=prods[0].id,exclude=False)

                base_image = False
                if len(prod_images) > 0:
                    base_image = prod_images[0]

                values.append({'product': tplproduct, 'name': tplproduct.name.lower(), 'product_variant': len(prods), 'price': prods[0].price, 'base_image': base_image})

            # == order by name or price ==
            values.sort(key=lambda x: x[request.session['order']], reverse = request.session['order_by'] == 'desc')

            # == template values ==
            title = _('%(category)s - Page %(page)s of %(total)s') % {'category': categories[0].name, 'page': products.number, 'total': products.paginator.num_pages}
            metadescription = _('%(category)s. Page %(page)s of %(total)s') % {'category': categories[0].description, 'page': products.number, 'total':products.paginator.num_pages}
            category_values = {
                'title': title,
                'category_title': categories[0].name,
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
            }
            return render_to_response("catalog/category.html", category_values, context_instance=RequestContext(request))
        else:
            raise Http404(_('This category is not available because you navigate with bookmarks or search engine. Use navigation menu'))
    else:
        raise Http404(_('This category is not available because you navigate with bookmarks or search engine. Use navigation menu'))

def product(request,product):
    """Product View"""

    kwargs = {
        'slug_'+get_language(): product, #slug is unique
        'productproduct__active': True,
    }

    product = get_object_or_404(ProductTemplate, **kwargs) #ProductTemplate
    products = ProductProduct.objects.filter(product_tmpl=product.id) #ProductProduct

    base_image = ProductImages.objects.filter(product__in=products, exclude=False, base_image=True) #Product Image Base
    thumb_images = ProductImages.objects.filter(product__in=products, exclude=False, base_image=False) #Product Image Thumbs

    if len(base_image) > 0:
        base_image = base_image[0]

    title = _('%(product)s') % {'product': product.name}
    metadescription = _('%(metadescription)s') % {'metadescription': product.metadescription}

    return render_to_response("catalog/product.html", {'title': title, 'metadescription': metadescription, 'product': product, 'products': products, 'base_image': base_image, 'thumb_images': thumb_images, 'url': LIVE_URL}, context_instance=RequestContext(request))
