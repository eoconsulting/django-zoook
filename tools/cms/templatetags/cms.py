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

from django import template
from django.utils.translation import get_language, ugettext as _

from settings import USER_ADD_APP, ADMIN_URI

register = template.Library()

@register.inclusion_tag('cms/tags/user_add.html', takes_context = True)
def render_useradd(context):
    values = []
    
    if 'user' in context:
        for app_add in USER_ADD_APP:
            app  = app_add['app'].split('.')
            model_edit = '%s.add_%s' % (app[0],app[1])
            if context['user'].has_perm(model_edit):
                values.append({'url':'/'+get_language()+app_add['url'],'string':app_add['string']})
        if context['user'].is_staff:
            values.append({'url':ADMIN_URI,'string':_('Go to Admin')})
    return {
        'values': values,
    }
