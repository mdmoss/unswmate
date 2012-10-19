#!/usr/bin/python

import matedb as db
import images as images

def render(users):
    result = '';

    for i in xrange (0, len(users), 3):
        group = users[i:i+3]

        result += '<div class="row-fluid">'

        for user in group:

            result += '<div class="span4">'
            result += '<div class="span6"><a href="?who=' + user + '">' + images.get_profile_picture(user) + "</a></div>\n"
            result += '<div class="span6"><br /><a href="?who=' + user + '"><p><b>' + db.get_data(user, 'name') + "</b></p></a></div>\n"
            result += '</div>'
        result += '<br />'
        result += '</div>'
       
    return result
