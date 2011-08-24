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

from django.contrib.syndication.views import Feed
from django.utils.translation import get_language

from catalog.models import ProductTemplate
from transurl import *
from config import *

class ProductFeed(Feed):
    title = SITE_TITLE
    link = "/%s/" % (catalog_url[get_language()])
    description = SITE_DESCRIPTION

    def items(self):
        return ProductTemplate.objects.order_by('-created_on')[:RSS_MAX]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description
