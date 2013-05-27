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

import os.path

zoook_root = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))

import logconfig
from django.utils.translation import ugettext_lazy as _

import re

DEBUG = False
TEMPLATE_DEBUG = DEBUG
DEVEL = DEBUG    # Is development enviroment?

"""
If you just need to serve the static file from django.contrib.staticfiles
including non DEBUG environment.
If DEBUG=True this value is ignored.
DISCLAIMER: Using this method is inefficient and insecure.
Do not use this in a production setting. Use this only for development and
testing environment with DEBUG=False.
"""
STATICFILES_IGNORE_DEBUG = True

MAINTENANCE_MODE = False
ROOT_URLCONF = 'django_zoook.urls'
ADMIN_URI = '/manager/'
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
        'TIMEOUT': 900,
        'OPTIONS': {
            'MAX_ENTRIES': 500
        }
    }
}
LOCALE_PATHS = (
    #'/django_zoook/locale',
)

"""
Site Django
"""
SITE_ID = 1

"""
Localization and locale
"""
TIME_ZONE = 'GMT'

ugettext = lambda s: s

#Edit your languages
LANGUAGE_CODE = 'es'
LANGUAGES = (
    ('en', ugettext('English')),
    ('es', ugettext('Spanish')),
)
DEFAULT_LANGUAGE = 1
LOCALE_URI = True
LOCALEURL_USE_ACCEPT_LANGUAGE = True
LOCALES =  {
    'en':'en_US',
    'es':'es_ES',
}

"""
Default Currency Sale Shop
"""
DEFAULT_CURRENCY = '$'

"""
Currency Position:
  'before' -> $ 999
  'after'  -> 999 $
"""
CURRENCY_LABEL_POSITION = 'before'

"""
Sale Order, when add product, continue if get warning
True: If get warning, not add product
False: If get warning, add product
"""
SALE_ORDER_PRODUCT_CHECK = True

"""
Sale Order, when add product with supply method
is produce, continue if get warning
True: If get warning, not add product
False: If get warning, add product
Note: If SALE_ORDER_PRODUCT_CHECK is False,
this variable is ignored
"""
SALE_ORDER_PRODUCE_PRODUCT_CHECK = False

"""
OpenERP Conf
"""
OERP_SALE = 1 #Sale Shop. All price, orders, ... use this Sale Shop ID.
OERP_SALES = [1,2] #Sale Shops. Orders by Sale Shops
OERP_COMPANY = 1 #Account Invoice. All invoices... use this Company ID.
COUNTRY_DEFAULT = 'ES'
PRODUCT_METADESCRIPTION = True
ATTACHMENT_SYNC = True
ATTACHMENT_SERVER = 'user@localhost'
ATTACHMENT_SERVER_PORT = '22'
ATTACHMENT_SSH_OPTION = ''
ATTACHMENT_RSYNC_OPTION = ''
ATTACHMENT_SOURCE = '/home/user/attach/openerp/'
ATTACHMENT_ROOT = '/home/user/attach/django/'

"""
Base template
"""
BASE_TEMPLATE = 'default'

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
        'PORT': '5432',         # Set to empty string for default. Not used with sqlite3.
    }
}

"""
OpenERP Webservice Connection
"""
OERP_CONF = {
    'username':'admin',
    'password':'admin',
    'dbname':'oerp_zoook',
    'protocol':'xmlrpc', #xmlrpc
    'uri':'http://localhost', #xmlrpc
    'port':8069, #xmlrpc
#    'protocol':'pyro', #pyro
#    'uri':'localhost', #pyro
#    'port':8071, #pyro
}

PROJECT_APPS = (
    'django_zoook.blog',
    'south',
    'transmeta',
    #'sermepa.sermepa',
    #'sermepa.sermepa_test',
    #'django_zoook.payment.sermepa',
    #'paypal.standard.ipn',
    #'django_zoook.payment.paypal',
    #'django_zoook.payment.pasat4b',
    #'django_zoook.payment.check',
    #'django_zoook.payment.cashondelivery',
    #'django_zoook.payment.banktransfer',
    #'django_zoook.payment.debit',
)

"""
Pagination values
"""
PAGINATION_DEFAULT_TOTAL = 9
PAGINATOR_ITEMS = [9,18,36]
PAGINATOR_ORDER_TOTAL = 5 #remember change this value in your order template
PAGINATOR_INVOICE_TOTAL = 5 #remember change this value in your invoice template
PAGINATOR_BLOG_TOTAL = 5 #remember change this value in your blog template
PAGINATOR_MANUFACTURER_TOTAL = 49
PAGINATOR_DEFAULT_MODE = 'grid' # 'grid' or 'list'

"""
Project User Add APP
"""
PROJECT_USER_ADD_APP = [
    {'app':'django_zoook.blog.blog','url':'/blog/add/','string':'Add Blog'},
    {'app':'django_zoook.catalog.producthome','url':'/catalogmanage/producthome/','string':'Prod. Home'},
    {'app':'django_zoook.catalog.productrecommended','url':'/catalogmanage/productrecommended/','string':'Prod. Recommended'},
    {'app':'django_zoook.catalog.productoffer','url':'/catalogmanage/productoffer/','string':'Prod. Offer'},
]

"""
Project locale independent paths
"""
PROJECT_LOCALE_INDEPENDENT_PATHS  = ()

"""
Email conf
"""
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
#EMAIL_PORT = 587
EMAIL_FROM = ''
EMAIL_REPPLY = ''

"""
Recaptcha keys
"""
RECAPTCHA_PUB_KEY = ""
RECAPTCHA_PRIVATE_KEY = ""

"""
Paypal Configuration
"""
PAYPAL_RECEIVER_EMAIL = ""
PAYPAL_CURRENCY = 'EUR'

"""
Sermepa/Servired Configuration
"""
SERMEPA_URL_PRO = 'https://sis.sermepa.es/sis/realizarPago'
SERMEPA_URL_TEST = 'https://sis-t.sermepa.es:25443/sis/realizarPago'
SERMEPA_MERCHANT_URL = "http://127.0.0.1:8000/payment/sermepa/ipn"
SERMEPA_MERCHANT_NAME = "My Company SL"
SERMEPA_MERCHANT_CODE = ''
SERMEPA_SECRET_KEY = ''
SERMEPA_BUTTON_IMG = '/static/images/icons/sermepa.png'
SERMEPA_TERMINAL = 1
SERMEPA_CURRENCY = 978
SERMEPA_TRANS_TYPE = 0 # 0 - Autorizacion / 1 - Preautorizacion / 2 - Confirmacion / 3 - Devolución Automatica / 4 - Pago Referencia / 5 - Transacción Recurrente / 6 - Transacción Sucesiva / 7 - Autenticación / 8 - Confirmación de Autenticación / 9 - Anulacion de Preautorizacion

"""
Passat 4b Configuration
"""
PASAT4B_MERCHANT_CODE = 'PI00000000'
PASAT4B_BUTTON_IMG = '/static/images/icons/passat4b.png'
PASAT4B_BUTTON_TEXT = 'Comprar ahora'
PASAT4B_DECIMAL = 2

"""
Twitter
"""
TWITTER_USER = 'zoook_esale'

"""
Google Analytics Key
"""
GOOGLE_ANALYTICS_KEY = ''
GOOGLE_ANALYTICS_IGNORE_ADMIN = True

"""
Image Thumbnail size
"""
THUMBNAIL_SIZE = '800x520'


"""
Require VAT number on registration page
"""
PARTNER_VAT_REQUIRED = False

"""
Global Module Activation
"""
UPDATE_PRICE = True    # Active the update special price by ajax when the user is signed
NEWSLATTER_ON = False  # Active the Newslatter info. Not implemented yet
COMPARE_ON = False     # Active the "Add to Compare" function in products. Not implemented yet
ORDER_SHOW_VAT = True  # Show the Base and VAT price in "Orders" and "My Cart" views?
