#!/usr/bin/env python

import os.path
import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import unicodedata
import torndb

from mongoengine import connect
import models

from settings import settings
from urls import url_handlers

from tornado.options import define, options


class Application(tornado.web.Application):
    def __init__(self):

        tornado.web.Application.__init__(self, url_handlers, **settings)
        
        # Setup a mongo connection
        connect("blog")

        # Have one global connection to the blog DB across all handlers
        self.db = torndb.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
