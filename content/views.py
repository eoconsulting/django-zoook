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
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.utils.translation import ugettext as _

from settings import *

from content.models import *

import os

def content_detail(request, content):
    """Content Detail"""
    content = get_object_or_404(Content, slug=content, status=True)
    title = content.name
    metakeywords = content.metakey
    metadescription = content.metadesc
    tpl = content.template or 'default.html'
    if content.template is not 'default.html':
        if not os.path.exists(TEMPLATE_DIRS[0]+'/content/'+tpl):
            tpl = 'default.html'
    return render_to_response("content/"+tpl, {'title':title,'metakeywords':metakeywords,'metadescription':metadescription,'content':content,'url':LIVE_URL}, context_instance=RequestContext(request))
