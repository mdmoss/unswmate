#!/usr/bin/python

import sqlite3
conn = sqlite3.connect('unswmate.db')
c = conn.cursor()

def user_exists(user):
    t = (user, )
    if c.execute('SELECT * FROM users WHERE username=?', t).fetchone():
        return True
    return False

def get_all_mates(user):
    t = (user,)
    mates = [];
    for mate in c.execute('SELECT mate FROM mates WHERE user=?', t):
        mates.append(mate[0])
    return mates
    
def get_all_courses(user):
    t = (user,)
    courses = [];
    for course in c.execute('SELECT course FROM courses WHERE user=?', t):
        courses.append(course[0])
    return courses
    
def get_data(user, field):
    t = (user,)
    # I'm a bad man
    query = 'SELECT %s FROM users WHERE username=?' % field
    c.execute(query, t)
    res = c.fetchone()
    if res:
        return res[0]
    else:
        return ''

def set_data(user, field, value):
    t = (value, user,)
    query = 'UPDATE users SET %s=? WHERE username=? ' % field
    c.execute(query, t)
    conn.commit()

def get_user_data(user):
    fields = ['username', 'name', 'password', 'email', 'gender', 'degree', 'about', 'student_number']  
    data = {}
    for field in fields:
        data[field] = get_data(user, field)
    data['courses'] = get_all_courses(user);
    data['mates'] = get_all_mates(user);
    return data;

def search_like(term, field):  
    t = ('%' + term + '%',)
    results = []
    query = "SELECT username FROM users WHERE " + field + " LIKE ?"
    for result in c.execute(query, t):
        results.append(result[0])
    return results

def create_user(username, password, email):
    t = (username, password, email,)
    c.execute('INSERT INTO users (username, password, email) values (?, ?, ?)', t)
    conn.commit()
    
def add_mate(user, mate):
    t = (user, mate,)
    if not c.execute('SELECT * FROM mates WHERE user=? AND mate=?', t).fetchone():
        c.execute('INSERT INTO mates (user, mate) values (?, ?)', t)
        conn.commit()