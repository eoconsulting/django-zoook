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

from transmeta import TransMeta

import modules.enums as enums

class Modules(models.Model):
    """Category FAQ."""
    __metaclass__ = TransMeta

    name = models.CharField(_('name'), max_length=255)
    position = models.CharField(_('position'), max_length=255)
    description = models.TextField(verbose_name=_('description'))
    status = models.IntegerField(_('status'), choices=enums.MODULES_STATUS_CHOICES, default=enums.STATUS_INACTIVE, help_text=_("Only modules with their status set to 'Active' will be displayed."))

    class Meta:
        verbose_name = _('module')
        verbose_name_plural = _('modules')
        translate = ('description', )

    def __unicode__(self):
        return self.name
