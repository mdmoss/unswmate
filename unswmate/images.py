#!/usr/bin/python

import glob
import matedb as db
import config

def get_profile_picture(user):
    name = db.get_data(user, 'profile_picture')
    if name:
        return '<img src="' + config.data_dir + name + '">'
    return ''
   
def get_all_pictures(user):
    images = db.get_all_pictures(user)
    for i, image in enumerate(images):
        images[i] = config.data_dir + image
    return images
