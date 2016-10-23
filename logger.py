#!/usr/bin/env python

"""A tool which pretends to be bash, and reports entered 
commands to a logger instead of executing them"""

import cookielib
import datetime
import os
import signal
import urllib
import urllib2

logaddr = "http://127.0.0.1:8011"

def prompt_and_post():
    cookies = cookielib.CookieJar()
    opener  = urllib2.build_opener(
        urllib2.HTTPCookieProcessor(cookies))
    urllib2.install_opener(opener)
    signal.signal(signal.SIGALRM, lambda num, frame: exit())
    signal.alarm(60)

    while True:
        try: 
            cmd = raw_input("bash> ")
        except EOFError:
            return
        
        data = urllib.urlencode({
            "ip"        : os.environ.get("SSH_CONNECTION"),
            "user"      : os.environ.get("USER"),
            "cmd"       : cmd,
            "timestamp" : datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        })
        
        opener.open(urllib2.Request(logaddr, data))

if __name__ == "__main__":
    prompt_and_post()
