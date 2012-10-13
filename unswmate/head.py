#!/usr/bin/python

import config

from string import Template

def get_head():
    f = open(config.template_dir + 'head.template', 'r')
    t = Template(f.read())
    d = dict(asset_dir = config.asset_dir)
    return t.safe_substitute(d)
