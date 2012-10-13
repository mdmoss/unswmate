#!/usr/bin/python

import matedb as db
import images as images
import cgienv

def get_matelist(user):

    matelist = "";

    for mate in db.get_all_mates(user):
        matelist += '<div class="span2"><a href="' + cgienv.get_URL() + '?who=' + mate + '">' + db.get_data(mate, 'name') + images.get_profile_picture(mate) + "</a></div>\n"
        
    return matelist
