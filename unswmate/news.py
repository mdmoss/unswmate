#!/usr/bin/python

import matedb
import authbar
import safety
import tempy

def get_news_pane(user): 

    components = dict()
    login = authbar.get_current_login()

    if user in matedb.get_all_mates(login) or user == login:
        components['post_box'] = get_post_box(user)
    else:
        components['post_box'] = ''

    components['news_items'] = ''
    posts = matedb.get_news(user)
    # Sort by time. Could use a namedtuple, or a class. Could do lots of things...
    posts.sort(key=lambda item: item[4])
    posts.reverse()
    for post in posts:
        components['news_items'] += item_format(post)

    return tempy.substitute ('news.template', components)

def get_post_box(user):
    return tempy.substitute('news_post_box.template', {'user':user})

def item_format(post):
    # Post format: (user, poster, message, image, time, id)
    data = {}
    data['poster_name'] = matedb.get_data(post[1], 'name')
    data['message'] = post[2]
    if post[3]:
        data['image'] = '<p><img src="' + post[3] + '"></img></p>';
    else:
        data['image'] = ''

    login = authbar.get_current_login()

    if login in matedb.get_all_mates(post[0]) or post[0] == login:
        data['comment_form'] = get_comment_form(post[5])
    else:
        data['comment_form'] = ''

    data['comments'] = ''
    comments = matedb.get_comments(post[5])
    comments.sort(key=lambda item: item[2])
    comments.reverse()
    for comment in comments:
        data['comments'] += comment_format(comment)

    return tempy.substitute('news_item.template', data) 

def get_comment_form(news_item_id):
    return tempy.substitute('news_item_comment_form.template', {'news_item_id':news_item_id});

def comment_format(comment):
    data = {}
    data['user'] = matedb.get_data(comment[0], 'name')
    data['message'] = comment[1]
    return tempy.substitute('news_comment.template', data)

def do_news(request):
    poster = authbar.get_current_login()

    if 'user' in request:
        user = request['user'].value
    else:
        user = ''

    if 'message' in request:
        message = request['message'].value
    else:
        message = ''

    if 'image' in request:
        image = request['image'].value
    else:
        image = ''

    if user and message and poster:
        if poster in matedb.get_all_mates(user) or user == poster: 
            matedb.post_news(user, poster, safety.make_safe(message), safety.make_safe(image))

    return '<script type="text/javascript">window.location.href="unswmate.cgi?who=' + user + '"</script>'

def do_comment(request):
    poster = authbar.get_current_login()
    if 'news_item_id' in request:
        news_item_id = request['news_item_id'].value
    else:
        news_item_id = ''

    if 'message' in request:
        message = request['message'].value
    else:
        message = ''

    # Rip the value out of the resulting tuple, if it exists
    user = matedb.get_owner(news_item_id)
    if user:
        user = user[0]

    if news_item_id and message:
        if poster in matedb.get_all_mates(user) or user == poster:
            matedb.post_comment(news_item_id, poster, safety.make_safe(message))

    return '<script type="text/javascript">window.location.href="unswmate.cgi?who=' + user + '"</script>'
