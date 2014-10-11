#/usr/bin/python
# -*- coding: utf-8 -*-
#
import os
import posixpath
import urllib
import BaseHTTPServer
import logging
from SimpleHTTPServer import SimpleHTTPRequestHandler

# modify this to add additional routes
ROUTES = (
    # [url_prefix ,  directory_path]
    ['/data', '../../data'],
    ['',       '.']  # empty string for the 'default' match
)

class RequestHandler(SimpleHTTPRequestHandler):

    def translate_path(self, path):
        """translate path given routes"""

        # set default root to cwd
        root = os.getcwd()

        # look up routes and set root directory accordingly
        for pattern, rootdir in ROUTES:
            if path.startswith(pattern):
                # found match!
                path = path[len(pattern):]  # consume path up to pattern len
                root = rootdir
                break

        # normalize path and prepend root directory
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)

        path = root
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir):
                continue
            path = os.path.join(path, word)
        logging.info("path : %s" % path)

        return path

if __name__ == '__main__':
    BaseHTTPServer.test(RequestHandler, BaseHTTPServer.HTTPServer)
