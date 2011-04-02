import os
import logging

from google.appengine.ext        import webapp
from google.appengine.ext.webapp import template
from google.appengine.api        import users

class SiteHandler(webapp.RequestHandler):
    template_vars = {}
    template_path = ''
    user          = None

    def get(self, site_key):
        
        # add user to vars
        self.user = users.get_current_user()
        self.template_vars["user"] = self.user
        self.template_vars["logout_url"] = users.create_logout_url('/')
        
        # dispatch
        if site_key == '': self.list_sites()
        else             : return self.error(404)
        
        # render template
        self.response.out.write(
            template.render( 
                self.template_path,
                self.template_vars
            )
        )

    def list_sites(self):
        self.template_path = 'templates/site_list.html'
        self.template_vars["sites"] = ["FIXME", "FIXME"]
        
        