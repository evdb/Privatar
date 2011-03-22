from Crypto.Hash import MD5
import urlencoding # pip install -e 'git://github.com/nshah/python-urlencoding.git#egg=urlencoding'

class privatar():
    http_base  = 'http://www.privatar.org'
    https_base = 'https://privatar-org.appspot.com'


    def __init__(self, site_key, shared_secret):
        self.site_key      = site_key
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
        
        if not salt:
            salt = self.generate_salt( email_md5 )
        
        avatar_code = self.generate_avatar_code( email_md5, salt )
        
        if secure:
            base = self.https_base
        else:
            base = self.http_base
        
        url = "%s/avatar/%s" % ( base, avatar_code )

        if suffix:
            url += '.' + suffix

        if query:
            url += '?' + urlencoding.compose_qs( query, sort=True )

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
        
    def generate_avatar_code( self, email_md5, salt ):
        # create the hash to encrypt the email_md5 with
        one_time_pad = self.md5( salt, self.shared_secret )
        
        # encrypt the email_md5
        encrypted_md5 = self.xor_md5s( email_md5, one_time_pad )
        
        # get the first letter of the shared_secret
        first_letter = self.shared_secret[:1]
        
        return '-'.join( [ self.site_key, salt, first_letter, encrypted_md5 ] )
        