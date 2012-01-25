#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = 'django-zoook',
    description = '',
    download_url = 'https://www.github.com/fuzzy-id/django-zoook',
    install_requires = [
        'django-localeurl',
        'django-transmeta',
        'paramiko',
        'recaptcha-client',
        'Pyro'
        ],
    requires = [
        'ooop',
        'django-inplaceedit',
        'django-maintenancemode'
        ],
    dependency_links = [
        'https://github.com/zikzakmedia/ooop.git',
        'https://github.com/zikzakmedia/django-inplaceeditform.git',
        'https://github.com/zikzakmedia/django-maintenancemode.git'
        ]

)
