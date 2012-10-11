#!/usr/bin/python

import subprocess

def send(address, subject, message):
    p = subprocess.Popen (['mail', '-s', subject, address], stdin=subprocess.PIPE)
    p.communicate(input=message)
