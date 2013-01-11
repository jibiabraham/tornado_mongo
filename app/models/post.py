from mongoengine import *
from models import user

class Post(Document):
	"""Represents a single post"""
	title = StringField(max_length=120, required=True)
	author = ReferenceField(User, reverse_delete_rule=CASCADE)
	tags = ListField(StringField(max_length=30))
	comments = ListField(EmbeddedDocumentField(Comment))

class TextPost(Document):
	"""Describes a text post"""
	content = StringField()

class ImagePost(Document):
	"""Describes an image post"""
	image_path = StringField()

class LinkPost(Document):
	"""Describes a link post"""
	link_url = StringField()
	

# Define comments
class Comment(EmbeddedDocument):
	"""A comment associated with a post"""
	content = StringField()
	name = StringField(max_length=120)