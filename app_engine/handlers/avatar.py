import logging
import cgi
import re

from google.appengine.ext import webapp
from google.appengine.api.urlfetch import fetch
from google.appengine.api.memcache import Client
from google.appengine.api import images

from externals.privatar import privatar

from models import SharedSecret

class AvatarHandler(webapp.RequestHandler):

    param_renaming = {
        "s" : "size",
        "d" : "default",
        "f" : "forcedefault",
        "r" : "rating",
    }

    def setup(self):

        qs = {}

        # extract the request parameters and create a normal dict of them
        request_params = cgi.parse_qs( self.request.query_string )
        for key in request_params:
            qs[key] = request_params[key][0]
            
        # rename all parameters to be consistent
        for (old, to) in self.param_renaming.items():
            qs[to] = qs.pop(old, '')

        # size must be a number between 1 and 512. default 80
        try:
            size = int( qs.get( 'size', 80 ) )
        except ValueError:
            size = 80
        if not size:    size = 80
        if size < 1:    size = 1
        if size > 512:  size = 512

        qs['size'] = size
        
        self.qs = qs
        # logging.debug( self.qs )
        return 1


    def get(self):
        self.setup()

        # extract the gravatar MD5 from the privatar code
        gravatar_md5 = self.get_gravatar_md5()

        # request the gravatar image and return it (caching as we go)
        gravatar_url = "http://www.gravatar.com/avatar/%s" % gravatar_md5
        
        # add remaining query bits that we should sond to gravatar
        gravatar_url += '?' + self.gravatar_query_string()
        
        # serve the gravatar url
        self.serve_gravatar_url( gravatar_url )


    def gravatar_query_string(self):
        q =  'default=404'
        q += '&size=%s' % self.qs['size']
        if self.qs['rating']:
            q += '&rating=%s' % self.qs['rating']
        return q

    def get_gravatar_md5(self):
        # extract the privatar code from the url
        privatar_code = re.findall('/avatar/([^/.]+)', self.request.path)[0]

        # get the site_code
        site_code, number  = privatar.extract_site_code_and_number( privatar_code )

        # load the shared_secret dictionary for the site key
        shared_secret = SharedSecret.get_secret_for_site_code_and_number( site_code, number )
        if not shared_secret:
            raise Exception( "ERROR - something is wrong with your request" )
        
        # decrypt md5
        email_md5 = privatar.extract_email_md5( privatar_code, shared_secret );

        return email_md5


    def serve_gravatar_url( self, gravatar_url ):

        res = self.fetch_gravatar_url( gravatar_url )
        
        # TODO - handle If-not-modified responses

        # set the headers and the content for success
        if res.status_code == 200:
            self.response.headers['Content-Type'] = 'image/jpeg'
            self.response.out.write(res.content)
        else:
            self.serve_404()


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


    def serve_404(self):

        default = self.qs['default']

        if   default == '404'       : self.serve_404_response()
        elif default == 'mm'        : self.serve_mm_404_image()
        # elif default == 'identicon' : self.serve_mm_404_image() # TODO - add
        else                        : self.serve_privatar_404_image()


    def serve_404_response(self):
        return self.error(404)


    def serve_mm_404_image(self):
        return self.serve_asset_image( 'mm.png' )


    def serve_privatar_404_image(self):
        return self.serve_asset_image( '404.png' )


    def serve_asset_image(self, image_filename):
        size = self.qs['size']

        memcache = Client()
        memcache_key = 'serve_asset_image-%s-%s' % ( image_filename, size )

        content = memcache.get( memcache_key )
        
        if not content:
            image = images.Image( open('assets/' + image_filename).read() )
            image.resize( width=size, height=size )
            content = image.execute_transforms( output_encoding=images.PNG )
            memcache.set( memcache_key, content, time=86400 )
        
        self.response.headers['Content-Type'] = 'image/png'
        self.response.out.write(content)
        return
