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

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.utils.translation import ugettext as _

from settings import *
from tools.zoook import siteConfiguration

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
            site_configuration = siteConfiguration(SITE_ID)

            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            contact_text = form.cleaned_data['contact_text']
            check_captcha = captcha.submit(request.POST['recaptcha_challenge_field'], request.POST['recaptcha_response_field'], RECAPTCHA_PRIVATE_KEY, request.META['REMOTE_ADDR'])
            if check_captcha.is_valid is False:
                # Captcha is wrong show a error ...
                message = _('Error with captcha number. Copy the same number.')
            else:
                subject = _('Contact - %(name)s') % {'name':site_configuration.site_title}
                body = _('This email is generated with Contact Module from %(site)s\n\n%(name)s - %(email)s\n%(message)s') % {'site':site_configuration.site_title,'name':name,'email':email,'message':contact_text}

                if site_configuration.contact_email:
                    contact_email = site_configuration.contact_email.split(',')
                    if len(contact_email)==0:
                        contact_email = [contact_email]

                    try:
                        emailobj = EmailMessage(subject, body, EMAIL_FROM, to=contact_email, headers = {'Reply-To': EMAIL_REPPLY})
                        emailobj.send()
                        message = _('Thanks for your message. We will answer soon.')
                    except:
                        message = _('Error SMTP server send email. Sorry. Can you try later?')
                else:
                    message = _('Error. Configure yours emails contacts.')
        else:
            message = _('Sorry! This form is not valid. Try again.')

    html_captcha = captcha.displayhtml(RECAPTCHA_PUB_KEY)

    return render_to_response("contact/form.html", locals(), context_instance=RequestContext(request))
