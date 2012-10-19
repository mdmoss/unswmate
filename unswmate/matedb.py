#!/usr/bin/python

import sqlite3
import datetime
import time

conn = sqlite3.connect('data/unswmate.db')
c = conn.cursor()

# Exposed for safety checks in other modules
user_data_fields = ['username', 'name', 'email', 'gender', 'degree', 'about', 'student_number']

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

def get_all_users():
    users = []
    for user in c.execute('SELECT username FROM users'):
        users.append(user[0])
    return users

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
    data = {}
    for field in user_data_fields:
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

def create_user(username, password_hash, salt, email):
    t = (username, password_hash, salt, email,)
    c.execute('INSERT INTO users (username, password_hash, salt, email) values (?, ?, ?, ?)', t)
    conn.commit()
    set_data(username, 'gender', '')
    set_data(username, 'degree', '')
    set_data(username, 'about', '')
    set_data(username, 'student_number', '')
    set_data(username, 'name', username)
    
def add_mate(user, mate):
    t = (user, mate,)
    if not c.execute('SELECT * FROM mates WHERE user=? AND mate=?', t).fetchone():
        c.execute('INSERT INTO mates (user, mate) VALUES (?, ?)', t)
        conn.commit()

def get_course_members(course):
    t = (course,)
    members = []
    for member in c.execute('SELECT user FROM courses WHERE course=?', t):
        members.append(member[0])
    return members

def get_all_pictures(user):
    t = (user,)
    images = []
    for image in c.execute('SELECT image FROM images WHERE user=?', t):
        images.append(image[0])
    return images
    
def image_exists(image):
    t = (image, )
    if c.execute('SELECT * FROM images WHERE image=?', t).fetchone():
        return True
    return False
    
def add_image(user, image):
    t = (user, image,)
    if not c.execute('SELECT * FROM images WHERE user=? AND image=?', t).fetchone():
        c.execute('INSERT INTO images (user, image) VALUES (?, ?)', t)
        conn.commit()   
        
privacy_fields = ['name', 'gender', 'student_number', 'degree', 'about', 
              'profile_picture', 'gallery', 'courses', 'matelist', 'news']
        
def is_private (user, property):
    t = (user, property,)
    if c.execute('SELECT * FROM privacy WHERE user=? AND property=?', t).fetchone():
        return True
    return False    
    
def make_private (user, property):
    t = (user, property,)
    if not c.execute('SELECT * FROM privacy WHERE user=? AND property=?', t).fetchone():
        c.execute('INSERT INTO privacy (user, property) VALUES (?, ?)', t)
        conn.commit()
        
def make_public (user, property):
    t = (user, property,)
    if c.execute('SELECT * FROM privacy WHERE user=? AND property=?', t).fetchone():
        c.execute('DELETE FROM privacy WHERE user=? AND property=?', t)
        conn.commit()

def get_news (user):
    t = (user,)
    return c.execute('SELECT user,poster,message,image,time,id FROM news WHERE user=?', t).fetchall();

def post_news (user, poster, message, image):
    # This looks a litle murky. Gets the current unix time
    post_time = int(time.mktime(datetime.datetime.now().timetuple()))
    t = (user, poster, message, image, post_time,)
    c.execute('INSERT INTO news (user, poster, message, image, time) VALUES (?, ?, ?, ?, ?)', t)
    conn.commit()

def news_item_exists(news_id):
    t = (news_id,)
    if c.execute('SELECT * FROM news WHERE id=?', news_id).fetchone():
        return True
    return False

def get_comments (news_id):
    t = (news_id,)
    return c.execute('SELECT user,message,time FROM comments WHERE news_id=?', t).fetchall();

def post_comment (news_id, user, message):
    post_time = int(time.mktime(datetime.datetime.now().timetuple()))
    t = (news_id, user, message, post_time,)
    c.execute('INSERT INTO comments (news_id, user, message, time) VALUES (?, ?, ?, ?)', t)
    conn.commit()
 
def get_owner (news_id):
    t = (news_id,)
    return c.execute('SELECT user FROM news WHERE id=?', t).fetchone()
