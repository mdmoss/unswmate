#!/usr/bin/python
import os
import cgi
import Cookie
from string import Template
import hashlib

import matedb as db
import head
import cgienv
import config

secret = "KVHJ)(*&^%$#QAXCVBNMKUYTRDFGHKL<MNBVFILOVEPERLILOVEPERLILOVEPERL"

def get_current_login():
    try:
        cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
        username = cookie["login"].value
        token = cookie["token"].value
        if token == get_token(username):
            return username
        return None
    except (Cookie.CookieError, KeyError):
        return None;
        
def do_login(request):
    if 'username' in request and 'password' in request:
        username = request['username'].value
        password = request['password'].value
        if db.get_data(username, 'password_hash') == get_hash(username, password):
            # Successful login
            print head.get_head()
            f = open(config.template_dir + 'authbar_login.template', 'r')
            t = Template (f.read())
            return t.safe_substitute(login=username, token = get_token(username), page=cgienv.get_full_URL())
      
def get_token(username):
    return hashlib.sha512(username + secret).hexdigest()

def do_logout(request):
    print head.get_head()
    f = open(config.template_dir + 'authbar_logout.template', 'r')
    t = Template (f.read())
    return t.safe_substitute()

def get_auth_menu_label():
    if get_current_login():
        return db.get_data(get_current_login(), 'name')
    else:
        return "login"

def get_auth_menu():
    menu = ""
    if get_current_login():
        # A user is logged in
        menu += '<li><a tabindex="-1" href="?who=' + get_current_login() + '">My Page</a><li>\n'
        menu += '<li class="divider"></li>'
        menu += '<li><a tabindex="-1" href="?action=logout">logout</a><li>\n'
    else:
        menu += '<li><a tabindex="-1" href="?action=create">New Account</a><li>\n'
        menu += '<li class="divider"></li>'
        menu += '<li>'
        menu += '<form method="post">'
        menu += '<input type="hidden" name="action" value="login">'
        menu += '<input type="text" name="username" class="input" placeholder="Username">'
        menu += '<input type="password" name="password" class="input" placeholder="Password">'
        menu += '<button type="submit" class="btn">Login</button>'
        menu += '</form>'
        menu += '</li>'
    return menu


def get_authbar():
    f = open(config.template_dir + 'authbar_top.template', 'r')
    t = Template (f.read())

    d = dict (
        auth = get_current_login(),
        auth_menu_label = get_auth_menu_label(),
        auth_menu_contents = get_auth_menu()
    )

    return t.safe_substitute(d)

def get_hash(user, password):
    salt = db.get_data(user, 'salt')
    return hashlib.sha512(password + salt).hexdigest()






