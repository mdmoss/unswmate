#!/usr/bin/python

import matedb
import csemail
import authbar
import cgienv
import tempy

def handle(request):

    d = {}
    requester = authbar.get_current_login() 

    if requester and'user' in request:
        
        user = request['user'].value
        if 'token' not in request:

            user_address = matedb.get_data(user, 'email')
            if user_address == 'mdm@cse.unsw.edu.au':
                csemail.send(user_address, "UNSW Mate request", get_mate_message(user, requester))
            d['message'] = 'Mate request sent. Stay tuned...';
            d['link'] = '?who=' + user
            d['link_message'] = "Return to their page. Stalk mode engage!"

        else :
            # Make a mateship
            matedb.add_mate(user, requester)
            # This is a bit interesting. The order is actually reversed
            # because it's the other user loading the link
            
            d['message'] = 'Mate added!'
            d['link'] = '?who=' + user
            d['link_message'] = "Go to their page"
    else:
        d['message'] = 'User not found';
        
        if requester:
            d['link'] = '?who=' + requester
            d['link_message'] = "Back to my page..."
        else:
            d['link'] = ''
            d['link_message'] = "Return to UNSWMate"

    print tempy.render('mate.template', d)


def get_mate_message(user, requester):
    message = "Hi " + user + '\n' 
    message += "You have a new mate request from " + requester + '\n'
    message += "To accept the request, click the link below\n"
    message += cgienv.get_URL() + '?action=mate&user=' + user + '&token=8827345257845'
    return message

def get_control_panel(user):
    panel = '<form method="post"><br />'

    login = authbar.get_current_login()
    
    if user == login:
        panel += '<p class="text-success"><b>Me!</b></p>'
    elif user in matedb.get_all_mates(login):
        panel += '<p class="text-success"><b>Mates</b></p>'
    else:
        panel += '<button class="btn" type="submit">Send Mate Request</button>\n'
        panel += '<input type="hidden" name="action" value="mate">\n'
        panel += '<input type="hidden" name="user" value="' + user + '">\n'

    panel += '</form>'
    return panel

