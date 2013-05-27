#!/usr/bin/env python
# -*- coding: utf-8 -*-
############################################################################################
#
#    Zoook. OpenERP e-sale, e-commerce Open Source Management Solution
#    Copyright (C) 2011 Zikzakmedia S.L. (<http://www.zikzakmedia.com>). All Rights Reserved
#
#    Source Created: 2012-06-07
#    Author: Mariano Ruiz <mrsarm@gmail.com>,
#            Enterprise Objects Consulting (<http://www.eoconsulting.com.ar>)
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




from setuptools import setup, find_packages

setup(
    name = 'django_zoook',
    description = 'Django part of Zoook e-Sale.',
    download_url = 'https://github.com/eoconsulting/django-zoook',
    install_requires = [
        'Django>=1.4',
        'psycopg2',
        'Pillow',
        'django_localeurl',
        'django_transmeta',
        'paramiko',
        'recaptcha_client',
        'Pyro',
        'ooop',
        'django_inplaceedit',
        'django_maintenancemode',
        'feedparser',
        'django-pagination',
        'django-filebrowser',
        'python-magic',
        'django-googlytics',
        'South',
        ],
    extras_require = {
        'cache':  ['haystack'],
        'server': [
                'staticsfiles_ignoredebug',
                ],
    }
)
