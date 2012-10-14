#!/usr/bin/python

import matedb
import authbar
import tempy

def get_user_data(user):   
    requester = authbar.get_current_login()
    mates = matedb.get_all_mates(user)
    
    data = matedb.get_user_data(user)
    for property in data.keys():
        if private (user, property) and requester not in mates and requester != user:
            data[property] = ''
    
    return data
    
def private (user, property):
    return matedb.is_private(user, property)
    
def permitted (user, property):
    requester = authbar.get_current_login()
    mates = matedb.get_all_mates(user)
    
    return requester == user or requester in mates or not private (user, property)
    
def get_privacy_pane (user):
    if authbar.get_current_login() != user: 
        return ''
        
    states = dict()

    for field in matedb.privacy_fields:
        states[field + '_state'] = cb_state (user, field)
        
    return tempy.substitute ('privacy.template', states)
    
def get_privacy_tab (user):
    if authbar.get_current_login() != user: 
        return ''
    else:
        return '<li><a href="#privacy" data-toggle="tab">Privacy</a></li>'
       
def cb_state (user, property):
    if private (user, property):
        return 'checked="yes"'
    return ''
    
def do_privacy (request):
    user = authbar.get_current_login()          
              
    for field in matedb.privacy_fields: 
        if field in request:
            value = request[field].value
            if value == 'on':
                matedb.make_private(user, field)
        else:
            matedb.make_public(user, field)

    return '<script type="text/javascript">window.location.href="unswmate.cgi?who=' + user + '"</script>'