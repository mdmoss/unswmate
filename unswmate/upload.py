#!/usr/bin/python

import authbar
import os
import random
import string
import matedb as db
import config

def do_upload(request):
    fileitem = request['file']
    image_file_name = get_unique_image_name()
    user = authbar.get_current_login()
    
    if user and fileitem.filename:
        open(config.data_dir + image_file_name, 'wb').write(fileitem.file.read())
        db.add_image(user, image_file_name)
        if 'profile' in request:
            db.set_data(user, 'profile_picture', image_file_name)
       
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

def get_unique_image_name():
    image_name = ''
    
    # This format gives us 56^12 possible combinations. Gee, I hope that's enough...
    while not image_name or db.image_exists(image_name):
        random_id = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(12)])
        image_name = 'images/' + random_id + '.jpg'
        
    return image_name