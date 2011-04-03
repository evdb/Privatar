import os
import logging
import re

from google.appengine.ext        import webapp
from google.appengine.ext.webapp import template
from google.appengine.api        import users

from models import Person, Site, SharedSecret

class BaseHandler(webapp.RequestHandler):
    def __init__(self):
        super(BaseHandler, self).__init__()

        self.vars          = {}
        self.template_path = 'you_need_to_set_template_path'

        user = users.get_current_user()
        if user:
            self.person = Person.from_user(user)
            self.vars["person"] = self.person
            self.vars["logout_url"] = users.create_logout_url('/')

    def post(self, *args, **kwargs):
        self.get(*args, **kwargs)
        
    def get(self, *args, **kwargs):
        self.dispatcher(*args, **kwargs)
                    
        if self.response.status == 200:
            # check that the template exists
            full_template_path = 'templates/' + self.template_path
            if not os.path.exists(full_template_path):
                raise Exception( "Can't find template at '%s'" % full_template_path)

            # serve the template
            self.response.out.write(
                template.render( 
                    full_template_path,
                    self.vars
                )
            )
