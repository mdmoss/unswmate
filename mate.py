#!/usr/bin/python

import matedb
import csemail
import authbar
import cgienv
import tempy

def handle(request):

    d = {}

    if 'user' in request:
        requester = authbar.get_current_login() 
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
            d['message'] = 'Mate added!'
            d['link'] = '?who=' + user
            d['link_message'] = "Go to their page"
    else:
        d['message'] = 'User not found';
        d['link'] = '?who=' + requester
        d['link_message'] = "Back to my page..."

    print tempy.render('mate.template', d)


def get_mate_message(user, requester):
    message = "Hi " + user + '\n' 
    message += "You have a new mate request from " + requester + '\n'
    message += "To accept the request, click the link below\n"
    message += cgienv.get_URL() + '?action=mate&user=' + user + '&token=8827345257845'
    return message

def get_control_panel(user):
    panel = '<form method="post"><br />'

    if user in matedb.get_all_mates(authbar.get_current_login()):
        panel += '<p class="text-success"><b>Mates</b></p>'
    else:
        panel += '<button class="btn" type="submit">Send Mate Request</button>\n'
        panel += '<input type="hidden" name="action" value="mate">\n'
        panel += '<input type="hidden" name="user" value="' + user + '">\n'

    panel += '</form>'
    return panel

