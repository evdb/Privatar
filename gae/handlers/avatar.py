import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api.urlfetch import fetch

from externals.privatar import privatar

class AvatarHandler(webapp.RequestHandler):
    def get(self):
        logging.debug( 'path: %s' % self.request.path )

        # extract the gravatar MD5 from the privatar code
        gravatar_md5 = self.get_gravatar_md5()

        # request the gravatar image and return it (caching as we go)
        gravatar_url = "http://www.gravatar.com/avatar/%s" % gravatar_md5
        
        res = fetch( gravatar_url )
        # logging.debug( res.headers )
        
        # set the headers and the content
        self.response.headers['Content-Type'] = 'image=jpeg'
        self.response.out.write(res.content)


    def handle_exception(self, exception, debug_mode=False):
        super(AvatarHandler, self).handle_exception(exception, debug_mode)
        # return self.error(404)

    def get_gravatar_md5(self):
        return '00000000000000000000000000000000'
        
        # extract the privatar code from the url
        
        # get the md5 we should be requesting
        
        