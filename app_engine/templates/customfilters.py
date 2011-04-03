import logging

from google.appengine.ext import webapp
from externals.privatar import privatar

from models import SharedSecret
 
CACHED_PRIVATAR = None

def get_privatar():
    global CACHED_PRIVATAR        
    if not CACHED_PRIVATAR:
        # load the secret or return if there is none
        secret = SharedSecret.secret_for_site_key('privatar')
        if not secret: return None

        # create the privatar object and cache it
        CACHED_PRIVATAR = privatar( 'privatar', secret)
        CACHED_PRIVATAR.http_base = ''
                    
    return CACHED_PRIVATAR


def privatar_url_from_email(value):
    p = get_privatar()
    if p:   return p.url(email=value)
    else:   return ''

def privatar_url_from_md5(value):
    p = get_privatar()
    if p:   return p.url(email_md5=value)
    else:   return ''
 

register = webapp.template.create_template_register()
register.filter(privatar_url_from_email)
register.filter(privatar_url_from_md5)
