import logging
import re
import random
import string

from google.appengine.ext import db
from models import Site


class SharedSecret(db.Model):
    site         = db.ReferenceProperty(reference_class=Site, required=True, collection_name='shared_secret_set' )
    site_code    = db.StringProperty(required=True)
    number       = db.IntegerProperty(required=True)
    secret       = db.StringProperty(required=True)
    created      = db.DateTimeProperty(auto_now_add=True)


    @classmethod
    def new_for_site( cls, site ):
        # get the highest first number
        oldest = site.shared_secret_set.order('-created').get();
        if oldest:  highest_number = oldest.secret[0]
        else:       highest_number = 0

        # Increment and handle wrap around
        number = highest_number + 1
        if number > 9: number = 1

        # delete shared secret if it already exists
        existing = site.shared_secret_set.filter('number =', number).get();
        if existing: existing.delete()
        
        choices = string.ascii_letters + string.digits
        length = 80
        secret = str(number) + ''.join( random.choice(choices) for i in range( length - 1) )

        # create a new shared secret
        new = cls(
            site = site,
            site_code=site.site_code,
            number=number,
            secret=secret
        )
        new.put()

        return new
        
    @classmethod
    def get_secret_for_site_code( cls, site_code ):
        return cls.get_secret_for_site_code_and_number( site_code, 1 )
    
    @classmethod
    def get_secret_for_site_code_and_number( cls, site_code, number ):
        shared = cls.all().filter('site_code =', site_code).filter('number =', int(number)).get()
        if not shared: return None
        return shared.secret
        