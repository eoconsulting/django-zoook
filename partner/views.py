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

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.core.validators import email_re

from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login

from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login

from django.core.mail import EmailMessage

from recaptcha.client import captcha

from partner.models import *
from base.models import *

from settings import *
from tools.conn import conn_webservice
from tools.zoook import checkPartnerID, checkFullName, connOOOP

import base64

def is_valid_email(email):
    """Email validation"""

    return True if email_re.match(email) else False

def login(request):
    """Login Page and authenticate. If exists session, redirect profile"""

    if request.user.is_authenticated(): #redirect profile
        return HttpResponseRedirect("/partner/profile/")

    title = _('Login')
    metadescription = _('Account frontpage of %(site)s') % {'site':SITE_TITLE}

    if 'username' in request.POST and 'password1' in request.POST:
        username = request.POST['username']
        password = request.POST['password1']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request, user)
                redirect = '/partner/profile/'
                if 'redirect' in request.POST:
                    redirect = base64.b64decode(request.POST['redirect'])
                return HttpResponseRedirect(redirect)
            else:
                error = _('Sorry. Your user is not active.')
        else:
            error = _('Sorry. Your username or password is not valid.')

    form = UserCreationForm()
    if request.GET.get('next'):
        redirect = base64.b64encode(request.GET.get('next'))

    return render_to_response("partner/login.html", locals(), context_instance=RequestContext(request))

def register(request):
    """Registration page. If exists session, redirect profile"""

    if request.user.is_authenticated(): #redirect profile
        return HttpResponseRedirect("/partner/profile/")

    title = _('Create an Account')
    metadescription = _('Create an Account of %(site)s') % {'site':SITE_TITLE}

    if request.method == "POST":
        message = []
        users = ''
        emails = ''

        form = UserCreationForm(request.POST)
        data = request.POST.copy()

        username = data['username']
        email = data['email']
        password = data['password1']
        name = data['name']
        vat_code = data['vat_code']
        vat = data['vat']
        street = data['street']
        zip = data['zip']
        city = data['city']
        country = data['country']
        
        if data['password1'] == data['password2']:
            if form.is_valid():
                if len(username) < USER_LENGHT:
                    msg = _('Username is short. Minimum %(size)s characters') % {'size': USER_LENGHT}
                    message.append(msg)
                if len(password) < KEY_LENGHT:
                    msg = _('Password is short. Minimum %(size)s characters') % {'size': KEY_LENGHT}
                    message.append(msg)

                if is_valid_email(email):
                    # check if user not exist
                    users = User.objects.filter(username__exact=username)
                    emails = User.objects.filter(email__exact=email)
                else:
                    msg = _('Sorry. This email is not valid. Try again')
                    message.append(msg)

                check_captcha = captcha.submit(request.POST['recaptcha_challenge_field'], request.POST['recaptcha_response_field'], RECAPTCHA_PRIVATE_KEY, request.META['REMOTE_ADDR'])
                if check_captcha.is_valid is False: # captcha not valid
                    msg = _('Error with captcha number. Copy same number.')
                    message.append(msg)

                if users:
                    msg = _('Sorry. This user are exists. Use another username')
                    message.append(msg)
                if emails:
                    msg = _('Sorry. This email are exists. Use another email or remember password')
                    message.append(msg)

                #check if this vat exists ERP
                if not message:
                    conn = connOOOP()
                    if not conn:
                        error = _('Error connecting with our ERP. Try again or cantact us')
                        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

                    partner = conn.ResPartner.filter(vat__ilike=data['vat_code']+data['vat'])
                    if len(partner) > 0:
                        msg = _('Sorry. This VAT exists our ERP. Contact Us for create a new user')
                        error.append(msg)

                #check if this vat valid
                if not message:
                    vat = data['vat_code']+data['vat']
                    check_vat = conn_webservice('res.partner', 'dj_check_vat', [vat, OERP_SALE])

                    if not check_vat:
                        msg = _('Vat not valid. Check if vat is correct')
                        error.append(msg)
                
                #create new partner and user
                if not message:
                    # create partner
                    partner = conn.ResPartner.new()
                    partner.name = data['name']
                    partner.vat = vat
                    partner.dj_username = data['username']
                    partner.dj_email = data['email']
                    partner_id = partner.save()
                    
                    # create address partner
                    address_types = ['contact','invoice','delivery']
                    for address_type in address_types:
                        address = conn.ResPartnerAddress.new()
                        address.name = data['name']
                        address.partner_id = conn.ResPartner.get(partner_id)
                        address.type = address_type
                        address.street = data['street']
                        address.zip = data['zip']
                        address.city = data['city']
                        address.country_id = conn.ResCountry.get(data['country'])
                        address.email = data['email']
                        address_id = address.save()
                    
                    # create user
                    # split name: first_name + last name
                    name = data['name'].split(' ')
                    if len(name) > 1:
                        first_name = name[0]
                        del name[0]
                        last_name = " ".join(name)
                    else:
                        first_name = ''
                        last_name = data['name']
                    user = User.objects.create_user(username, email, password)
                    user.first_name = first_name
                    user.last_name = last_name
                    user.is_staff = False
                    user.save()

                    # create authProfile
                    authProfile = AuthProfile(user=user,partner_id=partner_id)
                    authProfile.save()

                    # send email
                    subject = _('New user added - %(name)s') % {'name':SITE_TITLE}
                    body = _("This is email automatically from %(site)s\n\nUsername: %(username)s\nPassword: %(password)s\n\n%(live_url)s\n\nPlease, don't answer this email") % {'site':SITE_TITLE,'username':username,'password':password,'live_url':LIVE_URL}
                    email = EmailMessage(subject, body, to=[email])
                    email.send()
                    # authentification / login user
                    user = authenticate(username=username, password=password)
                    auth_login(request, user)
                    return HttpResponseRedirect("/partner/profile/")
            else:
                msg = _("Sorry. Error form values. Try again")
                message.append(msg)
        else:
            msg = _("Sorry. Passwords don't match. Try again")
            message.append(msg)

    form = UserCreationForm()
    html_captcha = captcha.displayhtml(RECAPTCHA_PUB_KEY)
    vat_code = VAT_CODE

    countries = ResCountry.objects.all()
    country_default = COUNTRY_DEFAULT
    
    return render_to_response("partner/register.html", locals(), context_instance=RequestContext(request))

def remember(request):
    """Remember password"""

    message = []

    title = _('Remember')
    metadescription = _('Remember account of %(site)s') % {'site':SITE_TITLE}

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        data = request.POST.copy()

        email = data['email']

        check_captcha = captcha.submit(request.POST['recaptcha_challenge_field'], request.POST['recaptcha_response_field'], RECAPTCHA_PRIVATE_KEY, request.META['REMOTE_ADDR'])
        if check_captcha.is_valid is False: # captcha not valid
            msg = _('Error with captcha number. Copy same number.')
            message.append(msg)
        else:
            if is_valid_email(email):
                # check if user  exist
                users = User.objects.filter(email__exact=email)
                if len(users) > 0:
                    #create new password
                    key = User.objects.make_random_password(length=KEY_LENGHT)
                    # update password
                    user = User.objects.get(id=users[0].id)
                    user.set_password(key)
                    user.save()
                    # send email
                    subject = _('Remember username - %(name)s') % {'name':SITE_TITLE}
                    body = _("This is email automatically from %(site)s\n\nUsername: %(username)s\nPassword: %(password)s\n\n%(live_url)s\n\nPlease, don't answer this email") % {'site':SITE_TITLE,'username':user.username,'password':key,'live_url':LIVE_URL}
                    email = EmailMessage(subject, body, to=[user.email])
                    email.send()
                    email = ''
                    msg = _('A new password are you send it to %(email)s') % {'email':user.email}
                    message.append(msg)
                else:
                    msg = _('Sorry. This email not exist. Try again')
                    message.append(msg)
            else:
                msg = _('Sorry. This email is not valid. Try again')
                message.append(msg)

    form = UserCreationForm()
    html_captcha = captcha.displayhtml(RECAPTCHA_PUB_KEY)

    return render_to_response("partner/remember.html", locals(), context_instance=RequestContext(request))

@login_required
def profile(request):
    """Profile page"""
    full_name = checkFullName(request)

    title = _('Profile %(full_name)s') % {'full_name':full_name}
    metadescription = _('Account frontpage of %(site)s') % {'site':SITE_TITLE}

    return render_to_response("partner/profile.html", locals(), context_instance=RequestContext(request))

@login_required
def changepassword(request):
    """Change Password page"""

    title = _('Change password')
    metadescription = _('Change password of %(site)s') % {'site':SITE_TITLE}

    if request.method == "POST":
        error = ''

        form = UserCreationForm(request.POST)
        data = request.POST.copy()

        if data['password1'] == data['password2']:
            if len(data['password1']) >= KEY_LENGHT:
                # update password
                request.user.set_password(data['password1'])
                request.user.save()
                if request.user.email:
                    # send email
                    subject = _('New password added - %(name)s') % {'name':SITE_TITLE}
                    body = _("This is email automatically from %(site)s\n\nNew password: %(password)s\n\n%(live_url)s\n\nPlease, don't answer this email") % {'site':SITE_TITLE,'password':data['password1'],'live_url':LIVE_URL}
                    email = EmailMessage(subject, body, to=[request.user.email])
                    email.send()
                error = _("New password added")
            else:
                error = _("Sorry. Passwords need %(size)s characters or more. Try again") % {'size':KEY_LENGHT}
        else:
            error = _("Sorry. Passwords don't match. Try again")

    form = UserCreationForm()
    return render_to_response("partner/changepassword.html", locals(), context_instance=RequestContext(request))

@login_required
def partner(request):
    """Partner page"""
    partner_id = checkPartnerID(request)
    if not partner_id:
        error = _('Are you a customer? Please, contact us. We will create a new role')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))
    conn = connOOOP()
    if not conn:
        error = _('Error connecting with our ERP. Try again or cantact us')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    partner = conn.ResPartner.get(partner_id)
    address_invoice = conn.ResPartnerAddress.filter(type='invoice',partner_id=partner_id)
    address_delivery = conn.ResPartnerAddress.filter(type='delivery',partner_id=partner_id)

    title = _('User Profile')
    metadescription = _('User profile of %(site)s') % {'site':SITE_TITLE}
    
    return render_to_response("partner/partner.html", locals(), context_instance=RequestContext(request))
