from mongoengine import *

DEV = False

def open_db():
	connect("tumblelog")