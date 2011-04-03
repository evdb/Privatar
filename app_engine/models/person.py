import logging
import re

from google.appengine.ext import db

class Person(db.Model):
    email    = db.StringProperty(required=True)
    user_id  = db.StringProperty(required=True)
    created  = db.DateTimeProperty(auto_now_add=True)
