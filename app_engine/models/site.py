import logging
import re

from google.appengine.ext import db
from models import Person

class SiteKeyNotValid(Exception):
    pass

class SiteKeyTaken(Exception):
    pass


def site_key_validator(value):
    if not Site.is_key_valid(value):
        raise SiteKeyNotValid()
    return True


class Site(db.Model):
    site_key = db.StringProperty(required=True, validator=site_key_validator)
    owner    = db.ReferenceProperty(reference_class=Person, required=True)
    created  = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def is_key_valid( cls, key ):
        if re.match( '[a-z][a-z0-9\_]{5,19}$', key ):
            return True
        else:
            return False
        
    @classmethod
    def is_key_taken( cls, key ):
        if cls.all().filter( 'site_key =', key ).count(1):
            return True
        else:
            return False