#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/*
 * Copyright (C) 2017 DBC A/S (http://dbc.dk/)
 *
 * This is part of redirect-expander
 *
 * redirect-expander is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * redirect-expander is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

@author: mb-dbc-dk
"""
import re
import time
import tornado.httpserver
import tornado.ioloop
import tornado.web

from argparse import ArgumentParser
from random import randint, choice
from traceback import print_exc

class MainHandler(tornado.web.RequestHandler):
    VAR_MATCHER = re.compile('%\((.*?)(?::(.*?))?\)%')
    EXPANDERS = {'': lambda x: '%()%',
                 'NOW': lambda x: str(round(time.time() * 1000)),
                 'ONEOF': lambda x: MainHandler.one_of(x),
                 'RANDOM': lambda x: MainHandler.random_number(x)}
    
    def get(self, url):
        try:
            url = 'http:/' + self.expand_url() # url starts with /
            print("uri:", url)
            self.redirect(url)
        except Exception as e:
            print_exc()
            self.send_error(message=str(e))

    def expand_url(self):
        url = self.request.uri
        url = MainHandler.VAR_MATCHER.sub(MainHandler.expand_var, url)
        return url
 
    def write_error(self, status_code, **kwargs):
        if 'message' in kwargs.keys():
            self.finish("<html><title>%(code)d: %(message)s</title>"
                        "<body>%(msg)s</body></html>" % {
                            "code": status_code,
                            "message": self._reason,
                            "msg": kwargs.get('message')
                        })
        else:
            self.finish("<html><title>%(code)d: %(message)s</title>"
                        "<body>%(code)d: %(message)s</body></html>" % {
                            "code": status_code,
                            "message": self._reason,
                        })

    @staticmethod
    def expand_var(match):
        func = match.group(1)
        arg = match.group(2)
        if not func in MainHandler.EXPANDERS:
            raise Exception("Unknown expansion: " + func)
        f = MainHandler.EXPANDERS[func]
        return f(arg)

    RANDOM_MATCHER = re.compile("^\\s*(-?\\d+)(?:\\s*(?:,\\s*)?(-?\\d+))?\\s*$")
    @staticmethod
    def random_number(arg):
        a = 0
        b = 9
        if arg is not None:
            matcher = MainHandler.RANDOM_MATCHER.match(arg)
            if matcher is None:
                raise Exception("Illegal arguments to RANDOM: " + arg)
            if matcher.group(2) is None:
                b = int(matcher.group(1))
            else:
                a = int(matcher.group(1))
                b = int(matcher.group(2))
        return str(randint(min(a, b), max(a, b)))

    @staticmethod
    def one_of(arg):
        if arg is None:
            raise Exception("ONEOF: requires an argument")
        return choice(arg.split(";"))

if __name__ == "__main__":
    p = ArgumentParser(description="Expansion redirector")
    p.add_argument("-p", "--port", metavar="PORT", default=8888, dest="port", type=int,
                   help="Which port to listen to")
    p.add_argument("-d", "--doc-root", metavar="DIR", default="/tmp", dest="doc_root", type=str,
                   help="Where to serve index.html from")
    a = p.parse_args()
    s = tornado.httpserver.HTTPServer(
            tornado.web.Application([
                    (r"/()", tornado.web.StaticFileHandler, {
                            "path": a.doc_root,
                            "default_filename": "index.html"
                            }),
                    (r"/(.+/.*)", MainHandler),
                    ]))
    s.bind(a.port)
    s.start()
    line = "# Starting on port: %d #"%(a.port)
    bar = re.sub('.', '#', line)
    print(bar)
    print(line)
    print(bar)
    tornado.ioloop.IOLoop.current().start()
