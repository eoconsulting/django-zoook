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

from django import template

from zoook.modules.models import Modules

register = template.Library()

@register.inclusion_tag('modules/default.html')
def render_modules_user1():
    entry = ''
    entries = Modules.objects.filter(position='user1',status=True)
    if entries:
        entry = entries[0]
    return {
        'entry': entry,
    }

@register.inclusion_tag('modules/default.html')
def render_modules_user2():
    entry = ''
    entries = Modules.objects.filter(position='user2',status=True)
    if entries:
        entry = entries[0]
    return {
        'entry': entry,
    }

@register.inclusion_tag('modules/default.html')
def render_modules_user3():
    entry = ''
    entries = Modules.objects.filter(position='user3',status=True)
    if entries:
        entry = entries[0]
    return {
        'entry': entry,
    }

@register.inclusion_tag('modules/default.html')
def render_modules_user4():
    entry = ''
    entries = Modules.objects.filter(position='user4',status=True)
    if entries:
        entry = entries[0]
    return {
        'entry': entry,
    }

@register.inclusion_tag('modules/default.html')
def render_modules_user5():
    entry = ''
    entries = Modules.objects.filter(position='user5',status=True)
    if entries:
        entry = entries[0]
    return {
        'entry': entry,
    }

@register.inclusion_tag('modules/default.html')
def render_modules_user6():
    entry = ''
    entries = Modules.objects.filter(position='user6',status=True)
    if entries:
        entry = entries[0]
    return {
        'entry': entry,
    }

@register.inclusion_tag('modules/default.html')
def render_modules_user7():
    entry = ''
    entries = Modules.objects.filter(position='user7',status=True)
    if entries:
        entry = entries[0]
    return {
        'entry': entry,
    }

@register.inclusion_tag('modules/default.html')
def render_modules_user8():
    entry = ''
    entries = Modules.objects.filter(position='user8',status=True)
    if entries:
        entry = entries[0]
    return {
        'entry': entry,
    }

@register.inclusion_tag('modules/default.html')
def render_modules_left():
    entry = ''
    entries = Modules.objects.filter(position='left',status=True)
    if entries:
        entry = entries[0]
    return {
        'entry': entry,
    }

@register.inclusion_tag('modules/default.html')
def render_modules_right():
    entry = ''
    entries = Modules.objects.filter(position='right',status=True)
    if entries:
        entry = entries[0]
    return {
        'entry': entry,
    }
