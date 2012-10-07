#!/usr/bin/python

import matedb
import images
import cgienv

def get_matelist(user):

    matelist = "";

    for mate in matedb.get_all_mates(user):
        matelist += '<div class="span2"><a href="' + cgienv.get_URL() + '?who=' + mate + '">' + matedb.get_data(mate, 'name') + images.get_profile_picture(mate) + "</a></div>\n"
        
    return matelist
