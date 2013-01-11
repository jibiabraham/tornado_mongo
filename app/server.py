import os,site,sys
import logging

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.template
from tornado.options import options,define


ROOT = os.path.dirname(os.path.abspath(__file__))
path = lambda *a: os.path.join(ROOT, *a)

site.addsitedir(path('models'))

TEMPLATE_ROOT = path(ROOT, 'templates')

define("env", default='PRODUCTION', help="run on the given port", type=str)
define("port", default=9000, help="run on the given port", type=int)


class TM(tornado.web.Application):

    def __init__(self):

        app_settings = {
            "static_path": os.path.join(os.path.dirname(__file__), "static"),
            "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            "login_url": "/",
            "template_loader" : tornado.template.Loader(TEMPLATE_ROOT),
            "autoescape" : None,
            "xheaders" : True,
            "debug" : True
        }

        all_urls = list(urls.redirects)
        all_urls.extend(urls.url_patterns)

        tornado.web.Application.__init__(self, all_urls, **app_settings)

        tornado.options.parse_command_line()

def main():

    import models
    if len(sys.argv)>=2 and sys.argv[1] == '--env=DEV':
        models.db.DEV = True
        reload(models)

    models.db.open_db()

    options.logging = 'DEBUG'

    app = TM()
    http_server = tornado.httpserver.HTTPServer(app,xheaders=True)
    http_server.listen(options.port)

    #tornado.ioloop.IOLoop.instance().set_blocking_log_threshold(2)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
