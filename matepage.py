#!/usr/bin/python
import cgi
from string import Template

import matedb
import head
import matelist
import images         
import authbar 
import tempy
import gallery

def render():

    form = cgi.FieldStorage()
    if 'who' in form:
        user = form['who'].value
    else:
        user = ''

    if 'mood' in form and form['mood'].value == "sad":
        print '<iframe src="http://www.omfgdogs.com/" width="1920" height="1080" frameborder="0"></iframe>'

    data = dict(
        matelist = matelist.get_matelist(user),
        gallery = gallery.get_gallery(user),
        profile_picture = images.get_profile_picture(user),
    )

    data.update(matedb.get_user_data (user));

    return tempy.render('matepage.template', data)
