#!/usr/bin/env python

"""A tool which pretends to be bash, and reports entered 
commands to a logger instead of executing them"""

import cookielib
import datetime
import os
import threading
import urllib
import urllib2

logaddr = "http://127.0.0.1:8000"

def prompt_and_post():
    ip      = os.environ.get("SSH_CONNECTION")
    cookies = cookielib.CookieJar()
    opener  = urllib2.build_opener(
        urllib2.HTTPCookieProcessor(cookies))
    urllib2.install_opener(opener)

    while True:
        try: 
            cmd = raw_input("bash> ")
        except EOFError:
            return
        
        data = urllib.urlencode({
            "ip"        : ip,
            "cmd"       : cmd,
            "timestamp" : datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        })
        
        opener.open(urllib2.Request(logaddr, data))

if __name__ == "__main__":
    prompt_and_post()
