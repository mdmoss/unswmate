#!/usr/bin/python

from string import Template

import head
import matelist
import authbar

base = 'tempy_base.template'

# We can load all of these here, as this script is reloaded every
# time the page is. Makes me cry a little.
components = dict(
    head = head.get_head(),
    authbar = authbar.get_authbar()
)

def render (page, data):
    try:
        internal_page = open(page, 'r')
        t = Template(internal_page.read())
        components['content'] = t.safe_substitute(data)

        base_page = open(base, 'r')
        t = Template(base_page.read())
        return t.safe_substitute(components)  
    except:
        return ''
