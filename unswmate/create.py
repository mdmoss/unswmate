#!/usr/bin/python

import string
from string import Template
import hashlib
import random
import os
import re
import subprocess

import matedb as db
import tempy
import cgienv
import csemail

token = 'magic_token_I_am_too_lazy_to_store_serverside'

def do_create(request):

    form_contents = ""

    if token not in request:
        # They've just clicked the new link
        if 'email' not in request:
            # They've just clicked the new link
            form_contents += '<h3>Step 1: Supply a valid email address</h3>'
            form_contents += '<form method="post" action="unswmate.cgi?action=create">'
            form_contents += '<input type="hidden" name="action" value="create">'
            form_contents += '<input type="text" name="email" placeholder="Email" class="input-xlarge">'
            form_contents += '<br />'
            form_contents += '<button type="submit" class="btn">Submit</button>'
            form_contents += '</form>'
        else:

            # They're asking for an email to be sent, that's cool
            email = request['email'].value
            send_signup_email(email)

            form_contents += '<h3>Email sent. Check your inbox!</h3>'
     
    elif 'email' in request and 'username' not in request:
        # Actual Signup Time 
        form_contents = get_signup_form(request['email'].value)

    elif 'email' in request and 'username' in request and 'password' in request and token in request:

        if db.user_exists(request['username'].value) or not safe(request['username'].value):
            form_contents += "That usename is already taken. Try again"
            form_contents += get_signup_form(request['email'].value)
        else:
            # Actually do the account creation
            create_account(request['username'].value, request['password'].value, request['email'].value)
            form_contents += "<p>Account Created. Welcome to UNSW, mate</p>";
            form_contents += '<a href="?who=' + request['username'].value + '"><p>Go to my page</p></a>'

    d = dict (
        form = form_contents
    )

    return tempy.render('create.template', d);


def send_signup_email(email):
    msg = cgienv.get_URL() + '?action=create&email=' + email + '&' + token + '=1'
    csemail.send(email, 'UNSWMate Signup', msg)

def get_signup_form(email):
    form_contents = ""

    form_contents += '<h3>Step 2: Choose a username and password</h3>'
    form_contents += '<form method="post" action="unswmate.cgi?action=create">'
    form_contents += '<input type="hidden" name="action" value="create">'
    form_contents += '<input type="hidden" name="' + token + '" value="1">'
    form_contents += '<input type="hidden" name="email" value = "' + email +  '">'
    form_contents += '<input type="text" name="username" placeholder="Username">'
    form_contents += '<input type="password" name="password" placeholder="Password">'
    form_contents += '<button type="submit" class="btn">Submit</button>'
    form_contents += '</form>'

    return form_contents

def safe (username):
    if re.match('^\w+$', username):
        return True;
    return False;
    
def create_account(username, password, email):
    # Handle password hashing
    salt = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(12)])
    password_hash = hashlib.sha512(password + salt).hexdigest()
    
    db.create_user(username, password_hash, salt, email)
