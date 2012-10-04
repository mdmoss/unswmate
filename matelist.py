#!/usr/bin/python

import matedb

def get_matelist(user):

    matelist = "";

    for mate in matedb.get_all_mates(user):
        matelist = matelist + "<p>" + mate + "</p>\n"
        
    return matelist