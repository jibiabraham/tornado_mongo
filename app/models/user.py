from mongoengine import *

class User(Document):
	"""Defines a single user in the system"""
	email = StringField(required=True)
	first_name = StringField(max_length=True)
	last_name = StringField(max_length=True)
