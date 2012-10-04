#!/usr/bin/python

import sqlite3
conn = sqlite3.connect('unswmate.db')
c = conn.cursor()

def get_all_mates(user):
    t = (user,)
    mates = [];
    for mate in c.execute('SELECT * FROM mates WHERE user=?', t):
        mates.append(mate[2])
    return mates