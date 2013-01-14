import logging
import tornado
import tornado.template
import os
from handlers.response_handlers import EntryModule
from tornado.options import define, options


# Make filepaths relative to settings.
path = lambda root,*a: os.path.join(root, *a)
ROOT = os.path.dirname(os.path.abspath(__file__))

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=False, help="debug mode")
define("mysql_host", default="127.0.0.1:3306", help="blog database host")
define("mysql_database", default="blog", help="blog database name")
define("mysql_user", default="blog", help="blog database user")
define("mysql_password", default="blog", help="blog database password")

tornado.options.parse_command_line()

MEDIA_ROOT = path(ROOT, 'static')
TEMPLATE_ROOT = path(ROOT, 'templates')

settings = {
    'debug': options.debug,
    'static_path': MEDIA_ROOT,
    'cookie_secret': "your-cookie-secret",
    'xsrf_cookies': True,
    'template_loader': tornado.template.Loader(TEMPLATE_ROOT),
    'login_url': "/auth/login",
    'autoescape': None,
    'ui_modules': {"Entry": EntryModule},
}
