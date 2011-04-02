import os
import logging
import re

from google.appengine.ext        import webapp
from google.appengine.ext.webapp import template
from google.appengine.api        import users

from models import Site

class SiteHandler(webapp.RequestHandler):
    def __init__(self):
        super(SiteHandler, self).__init__()
        self.vars          = {}
        self.template_path = 'you_need_to_set_template_path'

        user = users.get_current_user()
        if user:
            self.user = user
            self.vars["user"] = self.user
            self.vars["logout_url"] = users.create_logout_url('/')

    def post(self, site_key):
        self.get(site_key)
        
    def get(self, site_key):
                
        # dispatch
        if   site_key == ''    : self.list_sites()
        elif site_key == 'add' : self.add_site()
        else                   : self.show_site(site_key)
        
        if self.response.status == 200:
    
            logging.debug( self.vars)
    
            # render template
            self.response.out.write(
                template.render( 
                    self.template_path,
                    self.vars
                )
            )

    def list_sites(self):
        self.template_path = 'templates/site_list.html'

        # find all matching sites
        sites = Site.all().filter('owner =', self.user).fetch(100)
        self.vars["sites"] = sites
    
    def add_site(self):
        self.template_path = 'templates/site_add.html'
        
        # get the site key
        site_key = self.request.get('site_key').strip()
        # site_key = re.sub('\s+', '', site_key)
        self.vars['site_key'] = site_key
        
        # return if there is no site_key, or we are not a post
        if (not site_key) or self.request.method != 'POST' :
            return
                    
        # check that the site_key is valid
        if not Site.is_key_valid( site_key ):
            self.vars['site_key_error'] = "site key is not valid"
            return
        
        # check that the site_key is valid
        if Site.is_key_taken( site_key ):
            self.vars['site_key_error'] = "site key already exists"
            return
        
        # ok to create
        site = Site( site_key=site_key )
        site.put()        
        self.redirect('/site/' + site_key )
        
    def show_site(self, site_key):
        self.template_path = 'templates/site_show.html'

        site = Site.all().filter( 'site_key =', site_key).get()
        
        if not site:
            return self.error(404)

        logging.debug( site )
        self.vars['site'] = site
        
        