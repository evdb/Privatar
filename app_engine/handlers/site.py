import os
import logging
import re

from google.appengine.ext        import webapp
from google.appengine.ext.webapp import template
from google.appengine.api        import users

from handlers import BaseHandler
from models import Person, Site, SharedSecret

class SiteHandler(BaseHandler):
    def dispatcher(self, site_key):
        if   site_key == ''    : self.list_sites()
        elif site_key == 'add' : self.add_site()
        else                   : self.show_site(site_key)

    def list_sites(self):
        self.template_path = 'site_list.html'

        # find all matching sites
        sites = self.person.site_set.fetch(100)
        self.vars["sites"] = sites
    
    def add_site(self):
        self.template_path = 'site_add.html'
        
        # get the site key
        site_key = self.request.get('site_key').strip()
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
        site = Site( site_key=site_key, owner=self.person )
        site.put()
        
        # create the first shared secret
        SharedSecret.new_for_site( site )
        
        self.redirect('/site/' + site_key )
        
    def show_site(self, site_key):
        self.template_path = 'site_show.html'

        site = self.person.site_set.filter( 'site_key =', site_key).get()
        
        if not site:
            return self.error(404)

        self.vars['site']    = site
        self.vars['secrets'] = site.shared_secret_set.order('-created').fetch(10)
        
        