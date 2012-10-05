#!/usr/bin/python
import os
import cgi
import Cookie
from string import Template

import matedb
import head

def get_current_login():
    try:
        cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
        return cookie["auth"].value
    except (Cookie.CookieError, KeyError):
        return None;
        
def do_login():
    c = cgi.FieldStorage()
    if 'username' in c and 'password' in c:
        username = c['username'].value
        password = c['password'].value
        # For now, we'll be lazy
        if matedb.get_data(username, 'password') == password:
            # Successful login
            print head.get_head()
            f = open('authbar_login.template', 'r')
            t = Template (f.read())
            print t.safe_substitute(auth=username)
            
def do_logout():
    print head.get_head()
    f = open('authbar_logout.template', 'r')
    t = Template (f.read())
    print t.safe_substitute()
            
def get_authbar():
    f = open('authbar_top.template', 'r')
    t = Template (f.read())
    return t.safe_substitute(auth=get_current_login())