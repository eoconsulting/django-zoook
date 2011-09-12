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

from django.utils.translation import ugettext_lazy as _

DEBUG = True

"""
Site Django
"""
SITE_ID = 1

"""
Localization and locale
"""
TIME_ZONE = 'Europe/Madrid'

ugettext = lambda s: s

#Edit your languages
LANGUAGE_CODE = 'es'
LANGUAGES = (
    ('en', ugettext('English')),
    ('es', ugettext('Spanish')),
    ('ca', ugettext('Catalan')),
)
DEFAUL_LANGUAGE = 1

"""
OpenERP Conf
"""
OERP_SALE = 1 #Sale Shop. All price, orders, ... use this Sale Shop ID.
OERP_COMPANY = 1 #Account Invoice. All invoices... use this Company ID.
VAT_CODE = ['ES']
COUNTRY_DEFAULT = 'ES'

"""
Log's conf
"""
LOGFILE = '/home/resteve/django/zoook/log/zoook.log' #path zoook log

"""
Base template
"""
BASE_TEMPLATE = 'default'

"""
Url's conf
"""
LIVE_URL = "http://127.0.0.1:8000/"
MEDIA_URL = "http://127.0.0.1:8000/static/"

"""
Database conf
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'dj_zoook',     # Or path to database file if using sqlite3.
        'USER': 'openerp',      # Not used with sqlite3.
        'PASSWORD': 'openerp',  # Not used with sqlite3.
        'HOST': 'localhost',    # Set to empty string for localhost. Not used with sqlite3.
#        'PORT': '5432',         # Set to empty string for default. Not used with sqlite3.
        'PORT': '5433',
    }
}

"""
OpenERP Webservice Connection
"""
OERP_CONF = {
    'username':'admin',
    'password':'admin',
    'dbname':'oerp6_zoook',
    'protocol':'xmlrpc', #xmlrpc
    'uri':'http://localhost', #xmlrpc
    'port':8051, #xmlrpc
#    'protocol':'pyro', #pyro
#    'uri':'localhost', #pyro
#    'port':8071, #pyro
}

"""
Email conf
"""
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True

"""
Captcha conf
"""
RECAPTCHA_PUB_KEY = ""
RECAPTCHA_PRIVATE_KEY = ""
