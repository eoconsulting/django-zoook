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

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from django.utils.translation import get_language
from transmeta import TransMeta

from datetime import datetime
import content.enums as enums

class ContentBase(models.Model):
    """Base class for models."""
    created_by = models.ForeignKey(User, null=True, editable=False, related_name="%(class)s_created_by", verbose_name=_('created by'))
    created_on = models.DateTimeField(_('created on'), default=datetime.now, editable=False)
    updated_on = models.DateTimeField(_('updated on'), editable=False)
    updated_by = models.ForeignKey(User, null=True, editable=False, verbose_name=_('updated by'))

class Content(ContentBase):
    """Content"""
    __metaclass__ = TransMeta

    name = models.CharField(_('Name'), max_length=256)
    slug = models.SlugField(_('slug'), max_length=128, help_text=_("This is a unique identifier that allows your contents to display its detail view, ex 'how-can-i-contribute'"), unique=True)
    description = models.TextField( _('description'))
    metadesc = models.TextField('metadesc')
    metakey = models.TextField('metakey')
    status = models.IntegerField(_('status'), choices=enums.STATUS_CHOICES, default=enums.STATUS_INACTIVE, help_text=_("Only contents with their status set to 'Active' will be displayed."))
    sort_order = models.IntegerField(_('sort order'), default=0, help_text=_('The order you would like the content to be displayed.'))
    template = models.CharField(max_length=256, help_text=_("If don't specific template, use default.html template"), blank=True)

    class Meta:
        verbose_name = _('content')
        verbose_name_plural = _('contents')
        ordering = ['-created_on']
        translate = (
            'name',
            'slug',
            'description',
            'metadesc',
            'metakey',
        )

    def __unicode__(self):
        return self.name

    def save(self):
        self.updated_on = datetime.now()
        super(Content, self).save()

    def get_absolute_url(self):
        return '/%s/%s' % (get_language(), self.slug)
