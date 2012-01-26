#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = 'django_zoook',
    description = '',
    download_url = 'https://www.github.com/fuzzy-id/django-zoook',
    install_requires = [
        'django',
        'psycopg2',
        'PIL',
        'django_localeurl',
        'django_transmeta',
        'paramiko',
        'recaptcha_client',
        'Pyro'
        ],
    requires = [
        'ooop',
        'django_inplaceedit',
        'django_maintenancemode'
        ]
)
