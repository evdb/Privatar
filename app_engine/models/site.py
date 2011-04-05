import logging
import re

from google.appengine.ext import db
from models import Person

class SiteCodeNotValid(Exception):
    pass

class SiteCodeTaken(Exception):
    pass


def site_code_validator(value):
    if not Site.is_code_valid(value):
        raise SiteCodeNotValid()
    return True


class Site(db.Model):
    site_code = db.StringProperty(required=True, validator=site_code_validator)
    owner     = db.ReferenceProperty(reference_class=Person, required=True)
    created   = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def is_code_valid( cls, code ):
        if re.match( '[a-z][a-z0-9\_]{5,19}$', code ):
            return True
        else:
            return False
        
    @classmethod
    def is_code_taken( cls, code ):
        if cls.all().filter( 'site_code =', code ).count(1):
            return True
        else:
            return False