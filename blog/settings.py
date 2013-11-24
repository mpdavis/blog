
import os


SETUP_COMPLETE = False
SETUP_IN_PROGRESS = False

SECRET_KEY = "S3CR3T"

ADMIN_EMAIL = 'mike.philip.davis@gmail.com'
ADMIN_NAME = 'Michael Davis'

DISQUS_SHORTNAME = 'michaeldavis'


uri = os.environ.get('MONGOLAB_URI', None)
if uri:
    uri_parts = uri.split('/')
    MONGODB_DB = MONGODB_USERNAME = uri_parts[3]
    sub_parts = uri_parts[2].split(':')
    MONGODB_PORT = sub_parts[2]
    MONGODB_PASSWORD, MONGODB_HOST = sub_parts[1].split('@')
else:
    MONGODB_HOST = None
    MONGODB_PORT = None
    MONGODB_DB = None
    MONGODB_USERNAME = None
    MONGODB_PASSWORD = None


try:
    from settingslocal import *
except ImportError:
    pass