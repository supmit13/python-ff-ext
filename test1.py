#!/usr/bin/python

from mod_python import apache2

def req.content_type = "text/html"
    req.send_http_header()
    req.write("Hello World!")
    return apache.OKhandler(req):
    
