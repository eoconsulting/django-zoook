# -*- coding: utf-8 -*-
############################################################################################
#
#    Zoook. OpenERP e-sale, e-commerce Open Source Management Solution
#    Copyright (C) 2011 Zikzakmedia S.L. (<http://www.zikzakmedia.com>). All Rights Reserved
#
#    Module Created: 24/04/2012
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


import logging
import sys
import os
from .config import zoook_root


"""
Log's conf
"""
LOGFILE = os.path.join(zoook_root, 'log', 'zoook.log') #path sync log
LOGLEVEL=logging.INFO

logging.basicConfig(filename=LOGFILE,level=LOGLEVEL, format='[%(asctime)s] %(levelname)-8s:%(filename)s:%(lineno)d: %(message)s', datefmt='%y-%m-%d %H:%M:%S')
console_log_handler = logging.StreamHandler()
console_log_handler.setFormatter(logging.Formatter('%(levelname)-8s:%(filename)s:%(lineno)d: %(message)s'))
logging.getLogger('').addHandler(console_log_handler)
