#!/usr/bin/python

import images
import privacy

def get_gallery(user):

    if not privacy.permitted (user, 'gallery'):
        return ''

    gallery = ""
    user_images = images.get_all_pictures(user)

    for i in xrange(0, len(user_images), 3):
        group = user_images[i:i+3]

        gallery += '<div class="row-fluid" id="gallery">'

        for image in group:
            gallery += '<div class="span4">'
            gallery += '<img src=' + image + '></img>'
            gallery += '</div>'

        gallery += '</div>'
         
    return gallery
