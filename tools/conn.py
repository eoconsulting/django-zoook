# -*- encoding: utf-8 -*-
############################################################################################
#
#    Zoook e-sale for OpenERP, Open Source Management Solution	
#    Copyright (C) 2011 Zikzakmedia S.L. (<http://www.zikzakmedia.com>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
############################################################################################

from ooop import OOOP
import xmlrpclib

# check if pyro is installed
try:
    import Pyro.core
except:
    pyro = False

from settings import OOOP_CONF

def connection():
    """Connection OpenERP with OOOP"""
    try:
        #o = OOOP(user='admin',pwd='admin',dbname='oerp6_zoook',uri='http://localhost',port=8069,protocol='xmlrpc')
        #o = OOOP(user='admin',pwd='admin',dbname='oerp6_zoook',uri='localhost',port=8071,protocol='pyro')
        conn = OOOP(user=OOOP_CONF['username'],pwd=OOOP_CONF['password'],dbname=OOOP_CONF['dbname'],uri=OOOP_CONF['uri'],port=OOOP_CONF['port'],protocol=OOOP_CONF['protocol'])
        return conn
    except:
        return False

def xmlrpc():
    """Connection OpenERP with XMLRPC"""
    try:
        # Get the uid
        server_common = '%s:%s/xmlrpc/common' % (OOOP_CONF['uri'],OOOP_CONF['port'])
        server_object = '%s:%s/xmlrpc/object' % (OOOP_CONF['uri'],OOOP_CONF['port'])

        sock_common = xmlrpclib.ServerProxy(server_common)
        uid = sock_common.login(OOOP_CONF['dbname'], OOOP_CONF['username'], OOOP_CONF['password'])
        return uid
    except:
        return False
