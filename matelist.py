#!/usr/bin/python

import matedb
import images

def get_matelist(user):

    matelist = "";

    for mate in matedb.get_all_mates(user):
        matelist = matelist + "<p>" + matedb.get_data(mate, 'name') + "</p>\n" + images.get_profile_picture(mate)
        
    return '<div class="span1">' + matelist + '</div>'