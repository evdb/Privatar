import logging
import re

from google.appengine.ext import db

class Person(db.Model):
    email    = db.StringProperty(required=True)
    user_id  = db.StringProperty(required=True)
    created  = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def from_user( cls, user ):
        """Find or create a person object for the user, and check email is correct"""

        user_id = user.user_id()
        email   = user.email()

        person = cls.all().filter( 'user_id =', user_id ).get()

        if person is None:
            person = cls( email=email, user_id=user_id )
            person.put()
        
        if person.email != email:
            person.email = email
            person.put()
        
        return person
        
