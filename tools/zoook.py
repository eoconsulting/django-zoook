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

from django.shortcuts import render_to_response
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required

from tools.conn import conn_ooop

""" Check Partner ID"""
@login_required
def checkPartnerID(request):
    try:
        partner_id = request.user.get_profile().partner_id
    except:
        partner_id = False
    return partner_id

""" Check Full Name"""
@login_required
def checkFullName(request):
    full_name = request.user.get_full_name()
    if not full_name:
        full_name = request.user
    return full_name

""" OOOP Connection"""
def connOOOP():
    conn = conn_ooop()
    return conn

""" OOOP Pagination"""
def paginationOOOP(request, total=0, limit=10):
    offset = 0
    page_previous = False
    page_next = False

    try:
        page = int(request.GET.get('page'))
        offset = limit*page
        page_previous = page-1
        if (page*limit)+limit < total: page_next = page+1
    except:
        page_previous = -1
        page_next = 1
    
    if total <= limit:
        page_next = False
        
    return offset, page_previous, page_next
