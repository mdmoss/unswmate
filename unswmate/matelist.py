#!/usr/bin/python

import matedb as db
import userlist
import authbar
import privacy

def get_matelist(user):

    if not privacy.permitted (user, 'matelist'):
        return ''

    return userlist.render(db.get_all_mates(user))
