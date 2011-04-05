#!/usr/bin/env python

import os
import logging

from google.appengine.dist import use_library
use_library('django', '1.2')

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from handlers import IndexHandler, AvatarHandler, SiteHandler, BaseHandler

# Load custom Django template filters
webapp.template.register_template_library('templates.customfilters')

def main():

    # determine if this is the dev server or not

    if BaseHandler.on_dev_server():     logging.getLogger().setLevel(logging.DEBUG)
    else:                   logging.getLogger().setLevel(logging.WARN)
      
    application = webapp.WSGIApplication(
        [
            ( '/avatar/.*',        AvatarHandler ),
            ( '/site/([^/]*).*',   SiteHandler ),
            ( '/.*',               IndexHandler  ),
        ],
        debug = BaseHandler.on_dev_server()      # only debug on dev server
    )

    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
