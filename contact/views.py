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

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.utils.translation import ugettext as _

from settings import *

from contact.models import *
from django.core.mail import EmailMessage

from recaptcha.client import captcha

def contactForm(request):
    """Contact Form"""
    title = _('Contact')
    message = ''

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            contact_text = form.cleaned_data['contact_text']
            check_captcha = captcha.submit(request.POST['recaptcha_challenge_field'], request.POST['recaptcha_response_field'], RECAPTCHA_PRIVATE_KEY, request.META['REMOTE_ADDR'])
            if check_captcha.is_valid is False:
                # Captcha is wrong show a error ...
                message = _('Error with captcha number. Copy same number.')
            else:
                subject = _('Contact - %(name)s') % {'name':SITE_TITLE}
                body = _('This is email generates with Contact Module from %(site)s\n\n%(name)s - %(email)s\n%(message)s') % {'site':SITE_TITLE,'name':name,'email':email,'message':contact_text}

                email = EmailMessage(subject, body, to=CONTACT_EMAIL)
                email.send()

                message = _('Thanks for your message. We will respond soon.')
        else:
            message = _('Sorry! This form is not valid. Try again.')

    html_captcha = captcha.displayhtml(RECAPTCHA_PUB_KEY)

    return render_to_response("contact/form.html", locals(), context_instance=RequestContext(request))
