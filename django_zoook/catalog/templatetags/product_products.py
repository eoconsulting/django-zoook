# -*- coding: utf-8 -*-
############################################################################################
#
#    Zoook. OpenERP e-sale, e-commerce Open Source Management Solution
#    Copyright (C) 2011 Zikzakmedia S.L. (<http://www.zikzakmedia.com>). All Rights Reserved
#    $Id$
#
#    Module Created: 2012-07-04
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

from django import template

register = template.Library()

@register.inclusion_tag('catalog/tags/product_products.html', takes_context = True)
def render_product_products(context):

    request = context['request']
    values = []
    for product in context['product_products']:
        url = product.product_tmpl.get_absolute_url()
        name = product.product_tmpl.name
        if product.product_tmpl.product_product_set.count() > 1:
            url += '?code=' + product.code.lower()
            name += ' - ' + product.variants
        base_image = product.get_base_image()
        values.append({
                'id': product.id,
                'product': product.product_tmpl,
                'name': name,
                'url': url,
                'price': product.get_price(),
                'price_normal': product.price,
                'price_special': product.price_special,
                'position': product.product_tmpl.position,
                'base_image': base_image
            })

    # == order by position, name or price ==
    try:
        values.sort(key=lambda x: x[request.session['order']], reverse = request.session['order_by'] == 'desc')
    except:
        pass

    context['values'] = values

    return context
