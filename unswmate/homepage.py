#!/usr/bin/python

import tempy
import userlist
import matedb
import random

def render():

    all_users = matedb.get_all_users()
    selection = []

    while len(selection) < 21:
        user = random.choice(all_users) 
        all_users.remove(user)
        selection.append(user)

    components = dict(
        users = userlist.render(selection)
    )

    return tempy.render('homepage.template', components)

