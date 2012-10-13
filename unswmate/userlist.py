#!/usr/bin/python

import matedb as db
import images as images

def format(users):
    result = "";

    for user in users:
        result += '<div class="span2"><a href="?who=' + user + '">' + db.get_data(user, 'name') + images.get_profile_picture(user) + "</a></div>\n"
        
    return result
