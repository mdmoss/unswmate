#!/usr/bin/python

from string import Template

import head
import matelist
import authbar

# We can load all of these here, as this script is reloaded every
# time the page is. Makes me cry a little.
components = dict(
    head = head.get_head(),
    authbar = authbar.get_authbar()
)

def render (page, data):
    try:
        f = open(page, 'r')
        t = Template(f.read())
        data.update(components)
        return t.safe_substitute(data)
    except:
        return ''