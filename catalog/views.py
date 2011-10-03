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

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils.translation import get_language
from django.db.models import Q
from django.utils import simplejson
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site

from settings import *
from tools.conn import conn_webservice
from tools.zoook import siteConfiguration, checkPartnerID, checkFullName, connOOOP

from catalog.models import *

@login_required
def updateprice(request):
    """
    B2B features
    Update Price catalog/product if partner are price rules different price rule sale shop.
    http://domain.com/catalog/updateprice/
    Return dicc elements ID product-price
    """

    data = ''
    if 'ides' in request.GET:
        product_ids = request.GET.get('ides').split(',') #get values ides

        if len(product_ids):
            try:
                partner_id = request.user.get_profile().partner_id
            except:
                partner_id = False

            if partner_id:
                products = []
                for product in product_ids:
                    products.append({'product_id':int(product),'quantity':1})
                # values => {"1":{"regularPrice":"50"},"2":{"regularPrice":"100"}}
                values = conn_webservice('product.product','zoook_compute_price', [OERP_SALE, products, partner_id])
                data = simplejson.dumps(values)
        
    return HttpResponse(data, mimetype='application/javascript')

def collect_children(category, level=0, children=None):
    """Category Children"""
    
    if children is None:
        children = []

    values = ProductCategory.objects.filter(parent=category).order_by('sequence')

    for i, child in enumerate(values):
        children.append((child.id, level))
        collect_children(child, level+1, children)

    return children

def pathcategory(category):
    """Category Path"""

    categories = ProductCategory.objects.filter(id=category)

    path = []
    path.append({'name':categories[0].name,'slug':categories[0].slug})

    while categories[0].parent:
        categories = ProductCategory.objects.filter(id=categories[0].parent.id)
        path.append({'name':categories[0].name,'fslug':categories[0].fslug})
    path.pop() #delete last category = firts category
    path.reverse()

    return path

def index(request):
    """
    Catalog Index
    All Categories list
    """

    root_category = ProductCategory.objects.filter(parent=None)

    values = []
    if len(root_category) > 0:
        categories = collect_children(root_category[0].id, 1, None)

        oldlevel = 0
        for (category, level) in categories:
            values.append((ProductCategory.objects.get(id=category), level, oldlevel))
            oldlevel = level

    site_configuration = siteConfiguration(SITE_ID)

    title = _('Categories')
    metadescription = _('List all categories of %s') % site_configuration.site_title
    return render_to_response("catalog/index.html", {'title': title, 'metadescription': metadescription, 'values': values}, context_instance=RequestContext(request))

def category(request,category):
    """All Products filtered by category"""

    values = []

    if category:
        kwargs = {
            'slug_'+get_language(): category, #slug is unique
            'status': True,
        }
        categories = ProductCategory.objects.filter(**kwargs)

        if len(categories)>0:
            categories_path = pathcategory(categories[0].id) #pathway
            products = ProductTemplate.objects.filter(Q(productproduct__active=True), Q(categ=categories[0]), Q(visibility='all') | Q(visibility='catalog'))

            # == Sessions Catalog ==
            # paginator options = session
            if 'paginator' in request.session:
                request.session['paginator'] = request.GET.get('paginator') and int(request.GET.get('paginator')) or request.session['paginator'] or PAGINATOR_TOTAL
            else:
                request.session['paginator'] = request.GET.get('paginator') and int(request.GET.get('paginator')) or PAGINATOR_TOTAL

            # mode options = session
            if 'mode' in request.session:
                request.session['mode'] = request.GET.get('mode') and request.GET.get('mode') or request.session['mode'] or 'grid'
            else:
                request.session['mode'] = request.GET.get('mode') and request.GET.get('mode') or 'grid'

            # order options = session
            if 'order' in request.session:
                request.session['order'] = request.GET.get('order') and request.GET.get('order') or request.session['order'] or 'price'
            else:
                request.session['order'] = request.GET.get('order') and request.GET.get('order') or 'price'

            # order_by options = session
            if 'order_by' in request.session:
                request.session['order_by'] = request.GET.get('order_by') and request.GET.get('order_by') or request.session['order_by'] or 'asc'
            else:
                request.session['order_by'] = request.GET.get('order_by') and request.GET.get('order_by') or 'asc'

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

                prod_images = ProductImages.objects.filter(product=prods[0].id,base_image=True)

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
                'categories_path': categories_path,
                'currency': DEFAULT_CURRENCY,
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
    }

    tplproduct = get_object_or_404(ProductTemplate, **kwargs) #ProductTemplate
    
    products = ProductProduct.objects.filter(product_tmpl=tplproduct.id) #ProductProduct
    product_attributes = ProductManufacturerAttribute.objects.filter(product=products[0].id) #ProductAttributes

    # get price and base_image product
    prods = ProductProduct.objects.filter(product_tmpl=tplproduct.id).order_by('price')

    prod_images = ProductImages.objects.filter(product=prods[0].id,exclude=False)
 
    base_image = False
    if len(prod_images) > 0:
        base_image = prod_images[0]
    
    base_image = ProductImages.objects.filter(product__in=products, exclude=False, base_image=True) #Product Image Base
    thumb_images = ProductImages.objects.filter(product__in=products, exclude=False, base_image=False) #Product Image Thumbs

    if len(base_image) > 0:
        base_image = base_image[0]

    title = _('%(product)s') % {'product': tplproduct.name}
    metadescription = _('%(metadescription)s') % {'metadescription': tplproduct.metadescription}
    
    search_keywords = tplproduct.metakeyword and tplproduct.metakeyword.split(',') or []
    metakeywords = tplproduct.metakeyword and tplproduct.metakeyword or ''

    #related
    related_products = []
    for product in tplproduct.related.all():
        products = ProductProduct.objects.filter(product_tmpl=product.id).order_by('price')
        related_products.append({'product':product, 'products':products})

    #upsells
    upsells_products = []
    for product in tplproduct.upsells.all():
        products = ProductProduct.objects.filter(product_tmpl=product.id).order_by('price')
        upsells_products.append({'product':product, 'products':products})

    values = {
        'title': title,
        'metadescription': metadescription,
        'metakeywords': metakeywords,
        'product': tplproduct,
        'products': prods,
        'related_products': related_products,
        'upsells_products': upsells_products,
        'price': prods[0].price,
        'base_image': base_image,
        'thumb_images': thumb_images,
        'search_keywords': search_keywords,
        'url': LIVE_URL,
        'currency': DEFAULT_CURRENCY,
    }
    return render_to_response("catalog/product.html", values, context_instance=RequestContext(request))

@login_required
def whistlist(request):
    """
    Whistlist
    Favourites products customer
    """

    partner_id = checkPartnerID(request)
    if not partner_id:
        error = _('Are you a customer? Please, contact us. We will create a new role')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    full_name = checkFullName(request)
    conn = connOOOP()
    if not conn:
        error = _('Error when connecting with our ERP. Try again or cantact us')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    prod_whistlist = False
    partner = conn.ResPartner.get(partner_id)
    product_obj = partner.product_whistlist_ids

    path = request.path_info.split('/')
    if 'remove' in path:
        kwargs = {
            'slug_'+get_language(): path[-1], #slug is unique
        }
        tplproduct = ProductTemplate.objects.filter(**kwargs)
        if len(tplproduct) > 0:
            try:
                for prod in product_obj:
                    if prod.id == tplproduct[0].id: #exist this product whistlist
                        prod_whistlist = conn_webservice('res.partner','write', [[partner_id], {'product_whistlist_ids':[(3, tplproduct[0].id)]}])
            except:
                prod_whistlist = True
                
    if 'add' in path:
        kwargs = {
            'slug_'+get_language(): path[-1], #slug is unique
        }
        tplproduct = ProductTemplate.objects.filter(**kwargs)
        if len(tplproduct) > 0:
            check_add = False
            if product_obj:
                for prod in product_obj:
                    if prod.id == tplproduct[0].id: #exist this product whistlist
                        check_add = True
            if not check_add:
                prod_whistlist = conn_webservice('res.partner','write', [[partner_id], {'product_whistlist_ids':[(4, tplproduct[0].id)]}])

    title = _('Whislist')
    metadescription = _('Whislist of %s') % full_name
    
    if prod_whistlist:
        partner = conn.ResPartner.get(partner_id) #refresh product_whistlist_ids if add or remove
        product_obj = partner.product_whistlist_ids
    
    products = []
    if product_obj:
        for prod in product_obj:
            prods = ProductProduct.objects.filter(product_tmpl=prod.id).order_by('price')
            tplproduct = ProductTemplate.objects.get(id=prod.id)
            prod_images = ProductImages.objects.filter(product=prod.id,exclude=False)
            base_image = False
            if len(prod_images) > 0:
                base_image = prod_images[0]

            products.append({'product': tplproduct, 'name': tplproduct.name, 'price': prods[0].price, 'base_image': base_image})

    return render_to_response("catalog/whistlist.html", {'title': title, 'metadescription': metadescription, 'products': products}, context_instance=RequestContext(request))

def compare(request):
    """
    Comparisation products
    """

    return render_to_response("catalog/compare.html", {'title': title, 'metadescription': metadescription, 'products': products}, context_instance=RequestContext(request))
