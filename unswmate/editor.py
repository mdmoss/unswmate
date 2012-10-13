#!/usr/bin/python

import authbar
import matedb as db
from string import Template
from safety import make_safe
import tempy

def do_edit(request):
    # This is where things get interesting
    user = authbar.get_current_login()
    if 'name' in request: 
        db.set_data(user, 'name', make_safe(request['name'].value)) 
    if 'about' in request: 
        db.set_data(user, 'about', make_safe(request['about'].value)) 
    if 'gender' in request: 
        db.set_data(user, 'gender', make_safe(request['gender'].value)) 
    if 'degree' in request: 
        db.set_data(user, 'degree', make_safe(request['degree'].value)) 
    if 'student_number' in request: 
        db.set_data(user, 'student_number', make_safe(request['student_number'].value)) 
    # Reload the edited page
    return '<script type="text/javascript">window.location.href="unswmate.cgi?who=' + user + '"</script>'

def render(user):
    if authbar.get_current_login() != user: 
        return ''

    # We know the user is logged in
    d = db.get_user_data(user)

    return tempy.substitute('editor.template', d)

def get_edit_tab(user):
    if authbar.get_current_login() == user:
        return '<li><a href="#edit" data-toggle="tab">Edit Profile</a></li>'
    else:
        return ''
