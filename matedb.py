#!/usr/bin/python

import sqlite3
conn = sqlite3.connect('unswmate.db')
c = conn.cursor()

def get_all_mates(user):
    t = (user,)
    mates = [];
    for mate in c.execute('SELECT mate FROM mates WHERE user=?', t):
        mates.append(mate[0])
    return mates
    
def get_all_courses(user):
    t = (user,)
    courses = [];
    for courses in c.execute('SELECT course FROM courses WHERE user=?', t):
        courses.append(course[0])
    return courses
    
def get_data(user, field):
    t = (user,)
    # I'm a bad man
    query = 'SELECT %s FROM users WHERE username=?' % field
    c.execute(query, t)
    if c.rowcount > 0:
        return c.fetchone()[0]
    else:
        return ''