import logging
import re
import random
import string

from google.appengine.ext import db
from models import Site


class SharedSecret(db.Model):
    site         = db.ReferenceProperty(reference_class=Site, required=True, collection_name='shared_secret_set' )
    site_key     = db.StringProperty(required=True)
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
            site_key=site.site_key,
            number=number,
            secret=secret
        )
        new.put()

        return new
        
    @classmethod
    def secret_for_site_key( cls, site_key ):
        latest = cls.all().filter('site_key =', site_key).filter('number =', 1).get()
        if not latest: return None
        return latest.secret
    
    