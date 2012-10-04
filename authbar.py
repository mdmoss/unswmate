#!/usr/bin/python
import os
import Cookie

import matedb

def get_current_login():
    try:
        cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
        print "user = " + cookie["user"].value
    except (Cookie.CookieError, KeyError):
        return None;
    
def 