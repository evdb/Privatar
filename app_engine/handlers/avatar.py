import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api.urlfetch import fetch
from google.appengine.api.memcache import Client
from google.appengine.api import images

from externals.privatar import privatar

class AvatarHandler(webapp.RequestHandler):
    def get(self):
        logging.debug( 'path: %s' % self.request.path )

        # extract the gravatar MD5 from the privatar code
        gravatar_md5 = self.get_gravatar_md5()

        # request the gravatar image and return it (caching as we go)
        gravatar_url = "http://www.gravatar.com/avatar/%s" % gravatar_md5
        gravatar_url += '?d=404'
        
        # serve the gravatar url
        self.serve_gravatar_url( gravatar_url )


    def get_gravatar_md5(self):
        # extract the privatar code from the url

        # get the site_key

        # load the shared_secret dictionary for the site key

        # decrypt md5

        return '00000000000000000000000000000002'


    def serve_gravatar_url( self, gravatar_url ):

        res = self.fetch_gravatar_url( gravatar_url )
        
        # TODO - handle If-not-modified responses

        # set the headers and the content for success
        if res.status_code == 200:
            self.response.headers['Content-Type'] = 'image/jpeg'
            self.response.out.write(res.content)
        else:
            self.serve_404_image()


    def fetch_gravatar_url( self, gravatar_url ):
        memcache = Client()
        res = memcache.get( gravatar_url )
        
        if not res:
            res = fetch( gravatar_url )
            memcache.set( gravatar_url, res, time=3600 )
        
        return res


    def handle_exception(self, exception, debug_mode=False):
        super(AvatarHandler, self).handle_exception(exception, debug_mode)
        # return self.error(404)


    def serve_404_image(self, size=80):
        # FIXME resize image to correct size
        memcache = Client()
        memcache_key = '404-image-%s' % size

        content = memcache.get( memcache_key )
        
        if not content:
            image = images.Image( open('assets/404.jpg').read() )
            image.resize( width=size, height=size )
            content = image.execute_transforms( output_encoding=images.JPEG )
            memcache.set( memcache_key, content, time=86400 )
        
        self.response.headers['Content-Type'] = 'image/jpeg'
        self.response.out.write(content)
        return
