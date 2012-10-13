#!/usr/bin/python

from string import Template

import config
import head
import matelist
import authbar

base = 'tempy_base.template'

# We can load all of these here, as this script is reloaded every
# time the page is. Makes me cry a little.
components = dict(
    authbar = authbar.get_authbar()
)

def render (page, data):
    try:
        internal_page = open(config.template_dir + page, 'r')
        t = Template(internal_page.read())
        components['content'] = t.safe_substitute(data)

        base_page = open(config.template_dir + base, 'r')
        t = Template(base_page.read())
        return t.safe_substitute(components)  
    except:
        return ''

def insert_head (page):
    return head.get_head() + "\n" + page

def substitute (page, data):
    try:
        template = open(config.template_dir + page, 'r')
        t = Template(template.read())
        return t.safe_substitute(data)  
    except:
        return ''
