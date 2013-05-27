#!/usr/bin/env python
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

import os
import sys

zoook_root = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.insert(0, zoook_root)
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_zoook.settings'

from django_zoook.settings import *
from django.utils.translation import ugettext as _

from django.contrib.sites.models import Site 
from django_zoook.tools.cms.models import SiteConfiguration

site = Site.objects.get(id=SITE_ID)
if site:
    values = {
        'site_ptr': site,
        'domain': site.domain,
        'name': site.name,
    }
    exclude_fields = ['id','domain','name','site_ptr']
    
    print "Add new configuration %s" % site.domain
    
    for field in SiteConfiguration._meta.fields:
        if field.name not in exclude_fields:
            if field.name == 'rss_max':
                values[field.name] = raw_input('%s (Leave blank to use 10): ' % field.name)
                if values[field.name] == '':
                    values[field.name] = '10'
            else:
                values[field.name] = raw_input('%s: ' % field.name)

    site_configuration = SiteConfiguration(**values)

    try:
        site_configuration.save()
        print "Add new site configuration: %s" % site_configuration.domain
        print "Start your Django APP: python manage.py runserver"
        print "Remember to clone Products and Categories OpenERP -> Django"
    except Exception, e:
        sys.stderr.write("Ups! Not save values? Try insert sql command...\n")
        sys.stderr.write("%s\n" % str(values))
        sys.stderr.write("Exception:\n%s\n" % e)
else:
    print "SITE ID Object not found"
