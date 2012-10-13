#!/usr/bin/python

import os

def get_URL():
    return os.getenv('SCRIPT_URI')

def get_params():
    return os.getenv('QUERY_STRING')

def get_full_URL():
    url = get_URL();
    if get_params():
        url += "?" + get_params()
    return url
