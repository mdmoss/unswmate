#!/usr/bin/python

import glob

def get_profile_picture(user):
    return '<img src="users/%s/profile.jpg" />' % user

def get_all_pictures(user):
    return glob.glob ('users/' + user + '/*.jpg')
