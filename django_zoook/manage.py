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

# Add the parent directory of 'manage.py' to the python path, so manage.py can
# be run from any directory. From http://www.djangosnippets.org/snippets/281/
import sys
zoook_root = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.insert(0, zoook_root)
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_zoook.settings'

from django.core.management import execute_manager
try:
    import settings # Assumed to be in the same directory.
    import logging
except Exception, e:
    sys.stderr.write('''Error: Can't find the file 'settings.py' in the directory containing %r.
It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.
(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n''' % __file__)
    sys.stderr.write(str("%s:\n%s\n" % (e.__class__.__name__, e)))
    sys.exit(-1)

if __name__ == "__main__":
    try:
        logging.info("Django Zoook starting")
        execute_manager(settings)
    except Exception, e:
        logging.error("Error starting Zoook\n%s:\n%s\n" % (e.__class__.__name__, e))
