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
import editor
import upload

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
        controls = get_control_panel(user),
        edit_pane_tab = editor.get_edit_tab(user),
        edit_pane_contents = editor.render(user),
        upload_pane_tab = upload.get_upload_tab(user),
        upload_pane_contents = upload.render(user),
    )

    data.update(matedb.get_user_data (user));

    return tempy.render('matepage.template', data)

def get_control_panel(user):
    panel = '<form><br />'

    if user in matedb.get_all_mates(authbar.get_current_login()):
        panel += '<b><p class="text-success">Already Mates</p></b>'
    else:
        panel += '<button class="btn">Send Mate Request</button>'
    
    panel += '</form>'
    return panel