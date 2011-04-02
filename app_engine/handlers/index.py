import os
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import main

allowed_paths = ['index', 'about']

class IndexHandler(webapp.RequestHandler):
    def get(self):
        
        # get the path and see if it can be made to match a template
        request_path  = self.request.path[1:] or 'index'
        template_path = 'templates/' + request_path + '.html'

        if request_path not in allowed_paths:
            return self.error(404)
                
        if not os.path.exists(template_path):
            return self.error(404)

        self.response.out.write(
            template.render( 
                template_path,
                {}
            )
        )
