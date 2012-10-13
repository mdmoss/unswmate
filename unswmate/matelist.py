#!/usr/bin/python

import matedb as db
import userlist

def get_matelist(user):

    return userlist.format(db.get_all_mates(user))
