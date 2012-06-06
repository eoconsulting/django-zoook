# -*- coding: utf-8 -*-
############################################################################################
#
#    Zoook. OpenERP e-sale, e-commerce Open Source Management Solution
#    Copyright (C) 2011 Zikzakmedia S.L. (<http://www.zikzakmedia.com>). All Rights Reserved
#
#    Module Created: 2012-06-06
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


import logging, datetime

root = logging.getLogger('')

def isdebug():
    return root.isEnabledFor(logging.DEBUG)

class TraceMiddleware(object):
    """
    Request / Response logging. Catch the unhandled exceptions.

    See http://djangosnippets.org/snippets/421/
    """

    def process_request(self, request):
        if isdebug():
            logging.debug(
                "%s %s" % (request.META['REQUEST_METHOD'],
                request.get_full_path())
            )
            request.started = datetime.datetime.now()
        return None

    def process_response(self, request, response):
        if isdebug():
            delta = (datetime.datetime.now() - request.started)
            logging.debug(
                "<- Response in: %f sec.",
                delta.seconds + (delta.microseconds / 1000000.0)
            )
        return response

    def process_exception(self, request, exception):
        logging.exception("Unhandled Exception:\n%s" % str(exception))
