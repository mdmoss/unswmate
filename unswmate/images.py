#!/usr/bin/python

import glob
import matedb as db
import config

def get_profile_picture(user):
    name = db.get_data(user, 'profile_picture')
    return '<img src="' + config.data_dir + name + '">'
    
def get_all_pictures(user):
    return glob.glob ('users/' + user + '/*.jpg')
