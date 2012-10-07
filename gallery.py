#!/usr/bin/python

import images

def get_gallery(user):
    gallery = ""
    for image in images.get_all_pictures(user):
        gallery += '<img src="' + image + '" />'
    return gallery
