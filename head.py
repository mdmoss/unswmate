#!/usr/bin/python

from string import Template

def get_head():
    f = open('head.template', 'r')
    t = Template(f.read())
    return t.safe_substitute()