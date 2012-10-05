#!/usr/bin/python
import cgi
from string import Template

import matedb
import head
import matelist
import images         
import authbar 
import tempy

def render():

    form = cgi.FieldStorage()
    if 'user' in form:
        user = form['user'].value
    else:
        user = ''

    if 'mood' in form and form['mood'].value == "sad":
        print '<iframe src="http://www.omfgdogs.com/" width="1920" height="1080" frameborder="0"></iframe>'

    data = dict(
    user_username = matedb.get_data(user, 'username'),
    user_profile_picture = images.get_profile_picture(user),
    user_name = matedb.get_data(user, 'name'),
    user_gender = matedb.get_data(user, 'gender'),
    user_degree = matedb.get_data(user, 'degree'),
    user_student_number = matedb.get_data(user, 'student_number'),
    matelist = matelist.get_matelist(user),
    )

    return tempy.render('matepage.template', data)