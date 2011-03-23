from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from externals.privatar import privatar

class AvatarHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('AvatarHandler')
