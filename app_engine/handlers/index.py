import os
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import main

from handlers import BaseHandler

allowed_paths = ['index', 'about', 'samples', 'gravatar']

class IndexHandler(BaseHandler):
    def dispatcher(self):

        # get the path and see if it can be made to match a template
        request_path  = self.request.path[1:] or 'index'
        template_path = request_path + '.html'

        if request_path not in allowed_paths:
            return self.error(404)

        self.template_path = template_path