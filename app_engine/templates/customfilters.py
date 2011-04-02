import logging

from google.appengine.ext import webapp
from externals.privatar import privatar
 
CACHED_PRIVATAR = None

def get_privatar():
    global CACHED_PRIVATAR        
    if not CACHED_PRIVATAR:
        logging.debug( 'setting up privatar object' )
        CACHED_PRIVATAR = privatar( 'privatar', 'FIXME' )
        CACHED_PRIVATAR.http_base = ''
                    
    return CACHED_PRIVATAR


def privatar_url_from_email(value):
    p = get_privatar()
    return p.url(email=value)

def privatar_url_from_md5(value):
    p = get_privatar()
    return p.url(email_md5=value)
 

register = webapp.template.create_template_register()
register.filter(privatar_url_from_email)
register.filter(privatar_url_from_md5)
