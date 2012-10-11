#!/usr/bin/python

import authbar
import os

def do_upload(request):
    fileitem = request['file']
    
    if fileitem.filename:
        if 'profile' in request:
            open('users/' + authbar.get_current_login() + '/profile.jpg', 'wb').write(fileitem.file.read())
        else:
            # strip leading path from file name to avoid directory traversal attacks
            fn = os.path.basename(fileitem.filename)
            open('users/' + authbar.get_current_login() + '/' + fn, 'wb').write(fileitem.file.read())
       
    return '<script type="text/javascript">window.location.href="unswmate.cgi?who=' + authbar.get_current_login() + '"</script>'
        

def render(user):
    if authbar.get_current_login() != user: 
        return ''
    else:
        return """<form enctype="multipart/form-data" method="post">
        <input type="file" name="file">
        <input type="hidden" name="action" value="upload">
        <br />
         <label class="checkbox">
            <input type="checkbox" name="profile"> Make this my profile picture
        </label>
        <button class="btn" type="submit">Upload</button>
        </form>
        """

def get_upload_tab(user):
    if authbar.get_current_login() != user: 
        return ''
    else:
        return '<li><a href="#upload" data-toggle="tab">Upload Images</a></li>'
