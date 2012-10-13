#!/usr/bin/python

import subprocess
import config

def send(address, subject, message):

    # Just a flag to prevent me accidently emailing strange addresses
    if config.email_restrict:
        if address not in config.email_whitelist:
            return
    
    p = subprocess.Popen (['mail', '-s', subject, address], stdin=subprocess.PIPE)
    p.communicate(input=message)
