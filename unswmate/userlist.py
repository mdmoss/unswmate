#!/usr/bin/python

import matedb as db
import images as images

def format(users):
    result = '';

    for i in xrange (0, len(users), 6):
        group = users[i:i+6]

        result += '<div class="row">'

        for user in group:
            result += '<div class="span2"><a href="?who=' + user + '"><p>' + db.get_data(user, 'name') + '</p>' + images.get_profile_picture(user) + "</a></div>\n"

        result += '</div>'
       
    return result
