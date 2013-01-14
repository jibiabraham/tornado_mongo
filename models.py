from mongoengine import *
import datetime

class User(Document):
	email = StringField(required=True)
	name = StringField()

class Entries(Document):
	published = DateTimeField(default=datetime.datetime.now)
	title = StringField()
	html = StringField()
	markdown = StringField()
	author = ReferenceField(User)
	slug = StringField(required=True)


