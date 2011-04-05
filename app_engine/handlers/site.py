import os
import logging
import re

from google.appengine.ext        import webapp
from google.appengine.ext.webapp import template
from google.appengine.api        import users

from handlers import BaseHandler
from models import Person, Site, SharedSecret

class SiteHandler(BaseHandler):
    def dispatcher(self, site_code):
        if   site_code == ''    : self.list_sites()
        elif site_code == 'add' : self.add_site()
        else                    : self.show_site(site_code)

    def list_sites(self):
        self.template_path = 'site_list.html'

        # find all matching sites
        sites = self.person.site_set.fetch(100)
        self.vars["sites"] = sites
    
    def add_site(self):
        self.template_path = 'site_add.html'
        
        # get the site code
        site_code = self.request.get('site_code').strip()
        self.vars['site_code'] = site_code
        
        # return if there is no site_code, or we are not a post
        if (not site_code) or self.request.method != 'POST' :
            return
                    
        # check that the site_code is valid
        if not Site.is_code_valid( site_code ):
            self.vars['site_code_error'] = "site code is not valid"
            return
        
        # check that the site_code is valid
        if Site.is_code_taken( site_code ):
            self.vars['site_code_error'] = "site code already exists"
            return
        
        # ok to create
        site = Site( site_code=site_code, owner=self.person )
        site.put()
        
        # create the first shared secret
        SharedSecret.new_for_site( site )
        
        self.redirect('/site/' + site_code )
        
    def show_site(self, site_code):
        self.template_path = 'site_show.html'

        site = self.person.site_set.filter( 'site_code =', site_code).get()
        
        if not site:
            return self.error(404)

        self.vars['site']    = site
        self.vars['secrets'] = site.shared_secret_set.order('-created').fetch(10)
        
        