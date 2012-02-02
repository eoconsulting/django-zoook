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

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from tools.zoook import siteConfiguration
from blog.models import *

from settings import *

import os

def blog_list(request):
    """
    All Blog
    """

    site_configuration = siteConfiguration(SITE_ID)

    blogs = Blog.objects.all().order_by('-created_on')
    blogs = blogs.filter(status=True)
    paginator = Paginator(blogs, PAGINATOR_TOTAL)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        blogs = paginator.page(page)
    except (EmptyPage, InvalidPage):
        blogs = paginator.page(paginator.num_pages)

    title = _('Blog :: All Posts. Page %(page)s of %(total)s') % {'page':blogs.number, 'total':blogs.paginator.num_pages}
    metadescription = _('List all post blog of %(site)s. Page %(page)s of %(total)s') % {'site':site_configuration.site_title, 'page':blogs.number, 'total':blogs.paginator.num_pages}

    return render_to_response("blog/list.html", {'title':title, 'metadescription': metadescription, 'blogs': blogs}, context_instance=RequestContext(request))

def blog_detail(request, blog):
    """Blog Detail"""
    kwargs = {
        'slug_'+get_language(): blog, #slug is unique
    }
    if not request.user.is_staff:
        kwargs['status'] = True
    blog = get_object_or_404(Blog, **kwargs)

    title = blog.name
    metakeywords = blog.metakey
    metadescription = blog.metadesc
    
    tpl = blog.template or 'default.html'
    if blog.template is not 'default.html':
        if not os.path.exists(TEMPLATE_DIRS[0]+'/blog/'+tpl):
            tpl = 'default.html'
    values = {
        'title':title,
        'metakeywords':metakeywords,
        'metadescription':metadescription,
        'blog':blog,
        'url': LIVE_URL,
    }

    return render_to_response("blog/"+tpl, values, context_instance=RequestContext(request))
