import logging
import re
import random
import string

from google.appengine.ext import db
from models import Site


class SharedSecret(db.Model):
    site         = db.ReferenceProperty(reference_class=Site, required=True, collection_name='shared_secret_set' )
    site_code    = db.StringProperty(required=True)
    version       = db.IntegerProperty(required=True)
    secret       = db.StringProperty(required=True)
    created      = db.DateTimeProperty(auto_now_add=True)


    @classmethod
    def new_for_site( cls, site ):
        # get the highest first version
        oldest = site.shared_secret_set.order('-created').get();
        if oldest:  highest_version = oldest.secret[0]
        else:       highest_version = 0

        # Increment and handle wrap around
        version = highest_version + 1
        if version > 9: version = 1

        # delete shared secret if it already exists
        existing = site.shared_secret_set.filter('version =', version).get();
        if existing: existing.delete()
        
        choices = string.ascii_letters + string.digits
        length = 40
        secret = str(version)
        secret += 'a'
        secret += ''.join( random.choice(choices) for i in range( length - len(secret) ) )

        # create a new shared secret
        new = cls(
            site = site,
            site_code=site.site_code,
            version=version,
            secret=secret
        )
        new.put()

        return new
        
    @classmethod
    def get_secret_for_site_code( cls, site_code ):
        return cls.get_secret_for_site_code_and_version( site_code, 1 )
    
    @classmethod
    def get_secret_for_site_code_and_version( cls, site_code, version ):
        shared = cls.all().filter('site_code =', site_code).filter('version =', int(version)).get()
        if not shared: return None
        return shared.secret
        