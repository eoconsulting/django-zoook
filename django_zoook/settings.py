# -*- coding: utf-8 -*-
############################################################################################
#
#    Zoook e-sale for OpenERP, Open Source Management Solution
#    Copyright (C) 2011 Zikzakmedia S.L. (<http://www.zikzakmedia.com>). All Rights Reserved
#    $Id$
#
#    Module Modified: 2012-06-07
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

import sys

from django_zoook.config import *

import os
import re

USER_ADD_APP = [
    {'app':'django_zoook.content.content','url':'/content/add/','string':'Add Content'},
    {'app':'django_zoook.cms.modules','url':'/cms/modules/list/','string':'All Modules'},
] + PROJECT_USER_ADD_APP

PAGINATOR_TOTAL = 9
PAGINATOR_ITEMS = [9,18,36]
PAGINATOR_ORDER_TOTAL = 5
PAGINATOR_INVOICE_TOTAL = 5

USE_THOUSAND_SEPARATOR = True

CATALOG_ORDERS = ['price','name']

USER_LENGHT = 8
KEY_LENGHT = 6

LOGIN_URL = '/partner/'
LOGIN_REDIRECT_URL = '/'

ADMINS = (
    ('Enterprise Objects Consulting','postmaster@mail.com'),
)

MANAGERS = ADMINS

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

PROJECT_PATH = os.path.dirname(__file__)
PATH = os.path.abspath(os.path.dirname(__file__).decode("utf-8"))

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PATH, "static")
#STATIC_ROOT = MEDIA_ROOT

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
STATIC_URL = '/static/'

STATICFILES_DIRS = (MEDIA_ROOT,)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'YOUR_SECRET_KEY'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'localeurl.middleware.LocaleURLMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'maintenancemode.middleware.MaintenanceModeMiddleware',
    'django_zoook.middleware.threadlocals.ThreadLocals', #local middleware project
    'django.middleware.cache.UpdateCacheMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
    'django_zoook.trace.TraceMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

TEMPLATE_DIRS = (
    os.path.join(PATH, "templates"+"/"+BASE_TEMPLATE),
    os.path.join(PROJECT_PATH,'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    # 'django.core.context_processors.auth',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django_zoook.tools.cms.context_processors.site_configuration',
    'django_zoook.tools.cms.context_processors.theme',
    'googlytics.context_processors.googlytics',
)

INSTALLED_APPS = (
    'localeurl',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    #'haystack',
    'inplaceeditform',
    'pagination',
    'django_zoook.base',
    'django_zoook.partner',
    'django_zoook.content',
    'django_zoook.contact',
    'django_zoook.catalog',
    'django_zoook.search',
    'django_zoook.tag',
    'django_zoook.account',
    'django_zoook.sale',
    'django_zoook.tools.filemanager',
    'django_zoook.tools.cms',
    'filebrowser',
    'googlytics',
) + PROJECT_APPS

AUTH_PROFILE_MODULE = "partner.AuthProfile"

LOCALE_INDEPENDENT_PATHS = (
    re.compile('^/static/'),
    re.compile('^/media/'),
    re.compile('^/manager/'),
    re.compile('^/filemanager/'),
    re.compile('^/filebrowser/'),
    re.compile('^/inplaceeditform/'),
) + PROJECT_LOCALE_INDEPENDENT_PATHS

MAINTENANCE_IGNORE_URLS = (
    r'^/static/*',
)

"""Search Engine"""
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}
