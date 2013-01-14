import markdown
import re
import os.path
import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import unicodedata

from models import *

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        user_email = self.get_secure_cookie("user")
        if not user_email: return None
        return User.objects(email=user_email).get()


class HomeHandler(BaseHandler):
    def get(self):
        entries = Entries.objects().all().order_by("-published").limit(5)
        if not entries:
            self.redirect("/compose")
            return
        self.render("home.html", entries=entries)


class EntryHandler(BaseHandler):
    def get(self, slug):
        entry = Entries.objects(slug=slug).get()
        if not entry: raise tornado.web.HTTPError(404)
        self.render("entry.html", entry=entry)


class ArchiveHandler(BaseHandler):
    def get(self):
        entries = Entries.objects().all().order_by("-published")
        self.render("archive.html", entries=entries)


class FeedHandler(BaseHandler):
    def get(self):
        entries = Entries.objects().all().order_by("-published").limit(10)
        self.set_header("Content-Type", "application/atom+xml")
        self.render("feed.xml", entries=entries)


class ComposeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        slug = self.get_argument("slug", None)
        print slug
        entry = None
        if slug:
            entry = Entries.objects(slug=slug).get()
        self.render("compose.html", entry=entry)

    @tornado.web.authenticated
    def post(self):
        slug = self.get_argument("slug", None)
        title = self.get_argument("title")
        text = self.get_argument("markdown")
        html = markdown.markdown(text)
        if slug:
            entry = Entries.objects(slug=slug)
            if not entry.get(): raise tornado.web.HTTPError(404)
            entry.update(set__title=title, set__markdown=text, set__html=html)
        else:
            slug = unicodedata.normalize("NFKD", title).encode(
                "ascii", "ignore")
            slug = re.sub(r"[^\w]+", " ", slug)
            slug = "-".join(slug.lower().strip().split())
            if not slug: slug = "entry"
            while True:
                e = Entries.objects(slug=slug).count()
                if e == 0: break
                slug += "-2"
            current_user = User.objects(email=self.current_user.email).get()
            entry = Entries(slug=slug, title=title, html=html, markdown=text, author=current_user)
            entry.save()
        self.redirect("/entry/" + slug)


class AuthLoginHandler(BaseHandler, tornado.auth.GoogleMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("openid.mode", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authenticate_redirect()

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Google auth failed")

        mongo_user = User.objects(email=user["email"])
        if mongo_user.first() == None:
            mongo_user = User(email=user["email"], name=user["name"])
            mongo_user.save()
        else:
            mongo_user = mongo_user.first()

        self.set_secure_cookie("user", str(mongo_user.email))
        self.redirect(self.get_argument("next", "/"))


class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))


class EntryModule(tornado.web.UIModule):
    def render(self, entry):
        return self.render_string("modules/entry.html", entry=entry)