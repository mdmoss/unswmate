#!/usr/bin/python

import images
import privacy

def get_gallery(user):

    if not privacy.permitted (user, 'gallery'):
        return ''

    gallery = ""
    for image in images.get_all_pictures(user):
        gallery += '<img src="' + image + '" />'
    return gallery
