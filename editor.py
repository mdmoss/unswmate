#!/usr/bin/python

import authbar
import matedb
from string import Template
from safety import make_safe

def do_edit(request):
    # This is where things get interesting
    user = authbar.get_current_login()
    if 'name' in request: 
        matedb.set_data(user, 'name', make_safe(request['name'].value)) 
    if 'about' in request: 
        matedb.set_data(user, 'about', make_safe(request['about'].value)) 
    if 'gender' in request: 
        matedb.set_data(user, 'gender', make_safe(request['gender'].value)) 
    if 'degree' in request: 
        matedb.set_data(user, 'degree', make_safe(request['degree'].value)) 
    if 'student_number' in request: 
        matedb.set_data(user, 'student_number', make_safe(request['student_number'].value)) 
    # Reload the edited page
    print '<script type="text/javascript">window.location.href="unswmate.cgi?who=' + user + '"</script>'

def render(user):
    if authbar.get_current_login() != user: 
        return ''

    # We know the user is logged in
    d = matedb.get_user_data(user)

    t = Template(open('editor.template', 'r').read())
    return t.safe_substitute(d)

def get_edit_tab(user):
    if authbar.get_current_login() == user:
        return '<li><a href="#edit" data-toggle="tab">Edit Profile</a></li>'
    else:
        return ''
