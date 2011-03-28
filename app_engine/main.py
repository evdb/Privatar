#!/usr/bin/env python

import os
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from handlers.index  import IndexHandler
from handlers.avatar import AvatarHandler


def main():

    # determine if this is the dev server or not
    try:
      is_dev = os.environ['SERVER_SOFTWARE'].startswith('Dev')
      logging.getLogger().setLevel(logging.DEBUG)
    except:
      is_dev = False
      logging.getLogger().setLevel(logging.WARN)


    application = webapp.WSGIApplication(
        [
            ( '/avatar/.*', AvatarHandler ),
            ( '/.*',        IndexHandler  ),
        ],
        debug=is_dev # olny debug on dev server
    )

    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
