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


DEBUG = True
MAINTENANCE_MODE = False

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
OpenERP Conf
"""
OERP_SALE = 1 #Sale Shop. All price, orders, ... use this Sale Shop ID.
OERP_COMPANY = 1 #Account Invoice. All invoices... use this Company ID.
COUNTRY_DEFAULT = 'AR'

"""
Base template
"""
BASE_TEMPLATE = 'default'

"""
Url's conf
"""
LIVE_URL = "http://dev.tienda.kikailabs.com.ar:8000/"
MEDIA_URL = LIVE_URL + "static/"

"""
Database conf
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'zoook_kikai',     # Or path to database file if using sqlite3.
        #'NAME': 'dj_zoook',     # Or path to database file if using sqlite3.
        'USER': 'zoook',      # Not used with sqlite3.
        'PASSWORD': 'postgres', # Not used with sqlite3.
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
    'dbname':'openerp6kikai',
    #'dbname':'openerp6dev',
    'protocol':'xmlrpc', #xmlrpc
    'uri':'http://localhost', #xmlrpc
    'port':8069, #xmlrpc
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
EMAIL_FROM = ''
EMAIL_REPPLY = ''

"""
Captcha conf
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
SERMEPA_MERCHANT_NAME = "Zikzakmedia SL"
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

"""
Global Module Activation
"""
UPDATE_PRICE = False    # Active the update special price by ajax when the user is signed
NEWSLATTER_ON = False  # Active the Newslatter info. Not implemented yet
COMPARE_ON = False     # Active the "Add to Compare" function in products. Not implemented yet
