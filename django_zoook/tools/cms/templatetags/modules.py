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

from django import template
from django.template import Library, Node
from django_zoook.tools.cms.models import Modules

register = template.Library()

class ModuleNode(Node):
    def __init__(self, tokens):
        self.tokens = tokens
 
    def render(self, context):
        entry = ''
        entries = Modules.objects.filter(position=self.tokens[0],status=True)
        if entries:
            entry = entries[0].description

        if len(self.tokens) > 1 and entry:
            div = "<div "
            for t in self.tokens[1:]:
                div += t + " "
            entry = div[:-1] + ">" + entry + "</div>"

        return entry

def module(parser, token):
    """
    Show Module data CMS:

    Basic tag Syntax::
        {% module POSITION [html_token1=value_token1 html_token2=value_token2 ...] %}

    *position* Key ID position Module

    IF HTML tokens are passed, the content is enclosed
    within <div html_token1=value_token1 html_token2=value_token2 ...> tag.

    Demo:
      {% module catalog.right %}
      {% module catalog.right id="catalog" class="border2" %}
    """

    parts = token.split_contents()

    if len(parts) < 2:
        raise template.TemplateSyntaxError(
            """'module' tag must be of the form:  {% module POSITION  [html_token1=value_token1 html_token2=value_token2 ...] %}""")

    return ModuleNode(parts[1:])

register.tag(module)
