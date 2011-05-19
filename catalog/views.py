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

    print values

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
            products = ProductTemplate.objects.filter(Q(productproduct__active=True),Q(categ=categories[0]), Q(visibility='all') | Q(visibility='catalog'))

            paginator = Paginator(products, TOTAL_PAGINATOR)

            try:
                page = int(request.GET.get('page', '1'))
            except ValueError:
                page = 1

            # If page request (9999) is out of range, deliver last page of results.
            try:
                products = paginator.page(page)
            except (EmptyPage, InvalidPage):
                products = paginator.page(paginator.num_pages)

            title = _('%(category)s - Page %(page)s of %(total)s') % {'category': categories[0].name, 'page': products.number, 'total': products.paginator.num_pages}
            metadescription = _('%(category)s. Page %(page)s of %(total)s') % {'category': categories[0].description, 'page': products.number, 'total':products.paginator.num_pages}
            return render_to_response("catalog/category.html", {'title':title, 'metadescription': metadescription, 'products': products}, context_instance=RequestContext(request))
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

    return render_to_response("catalog/product.html", {'title': title, 'metadescription': metadescription, 'product': product, 'products': products, 'base_image': base_image, 'thumb_images': thumb_images, 'url': URL_DOMAIN}, context_instance=RequestContext(request))
