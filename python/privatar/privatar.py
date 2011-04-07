import re
import urllib

from Crypto.Hash import MD5

class privatar():
    http_base  = 'http://www.privatar.org'
    https_base = 'https://privatar-org.appspot.com'


    def __init__(self, site_code, shared_secret):
        self.site_code     = site_code
        self.shared_secret = shared_secret    


    @classmethod
    def xor_md5s (cls, md5a, md5b ) :
        """Return the XOR result of the inputs"""
        return "%032x" % ( int(md5a, 16) ^ int(md5b, 16) )


    @classmethod
    def md5(cls, *input):        
        return MD5.new( '-'.join(input) ).hexdigest();


    def url( self, email=False, email_md5=False, secure=False, salt=False, query=False, suffix=False ):
        
        # get the email_md5 to use
        if email:
            email_md5 = self.md5( email )
        if not email_md5:
            raise Exception("Require either 'email' or 'email_md5'")      
        
        privatar_code = self.generate_privatar_code( email_md5, salt )
        
        if secure:
            base = self.https_base
        else:
            base = self.http_base
        
        url = "%s/avatar/%s" % ( base, privatar_code )

        if suffix:
            url += '.' + suffix

        if query:
            url += '?' + self._compose_qs( query )

        return url


    def generate_salt( self, email_md5 ):

        # create the md5 hash
        hash = self.md5( self.shared_secret, email_md5 )
        number = int(hash[:16], 16)

        alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'

        base36 = ''
        while number:
            number, i = divmod(number, 36)
            base36 = alphabet[i] + base36

        # keep it short
        return "%08s" % base36[:8]


    def generate_privatar_code( self, email_md5, salt=False ):
        # generate salt if needed
        if not salt:
            salt = self.generate_salt( email_md5 )
        
        # create the hash to encrypt the email_md5 with
        one_time_pad = self.md5( salt, self.shared_secret )
        
        # encrypt the email_md5
        encrypted_md5 = self.xor_md5s( email_md5, one_time_pad )
        
        # get the first letter of the shared_secret
        try:
            version = re.match( '(\d+)', self.shared_secret ).group(1)
        except IndexError:
            version = 0

        return '-'.join( [ self.site_code, str(version), salt, encrypted_md5 ] )


    @classmethod
    def extract_site_code_and_version( cls, code ):
        site_code, version, salt, encrypted_md5 = code.split('-')
        return site_code, version;


    @classmethod
    def extract_email_md5( cls, code, shared_secret ):
        site_code, version, salt, encrypted_md5 = code.split('-')
        one_time_pad = cls.md5( salt, shared_secret )        
        return cls.xor_md5s( encrypted_md5, one_time_pad );


    @classmethod
    def _compose_qs(cls, params):    
        # from git://github.com/nshah/python-urlencoding.git
        pieces = []
        for key in sorted(params):
            value = params[key]
            p = '%s=%s' % (cls._uri_escape(str(key)), cls._uri_escape(str(value)) )
            pieces.append(p)
        return '&'.join(pieces)


    @classmethod
    def _uri_escape(cls, value):
        return urllib.quote(value, safe='~')
