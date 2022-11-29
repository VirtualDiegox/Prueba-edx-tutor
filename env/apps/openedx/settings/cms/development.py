# -*- coding: utf-8 -*-
import os
from cms.envs.devstack import *

LMS_BASE = "openedx.untic-fibog.com:8000"
LMS_ROOT_URL = "http://" + LMS_BASE

# Authentication
SOCIAL_AUTH_EDX_OAUTH2_KEY = "cms-sso-dev"
SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT = LMS_ROOT_URL

FEATURES["PREVIEW_LMS_BASE"] = "preview.openedx.untic-fibog.com:8000"

####### Settings common to LMS and CMS
import json
import os

from xmodule.modulestore.modulestore_settings import update_module_store_settings

# Mongodb connection parameters: simply modify `mongodb_parameters` to affect all connections to MongoDb.
mongodb_parameters = {
    "host": "mongodb",
    "port": 27017,
    
    "user": None,
    "password": None,
    
    "db": "openedx",
    "replicaSet": None,
}
DOC_STORE_CONFIG = mongodb_parameters
CONTENTSTORE = {
    "ENGINE": "xmodule.contentstore.mongo.MongoContentStore",
    "ADDITIONAL_OPTIONS": {},
    "DOC_STORE_CONFIG": DOC_STORE_CONFIG
}
# Load module store settings from config files
update_module_store_settings(MODULESTORE, doc_store_settings=DOC_STORE_CONFIG)
DATA_DIR = "/openedx/data/modulestore"

for store in MODULESTORE["default"]["OPTIONS"]["stores"]:
   store["OPTIONS"]["fs_root"] = DATA_DIR

# Behave like memcache when it comes to connection errors
DJANGO_REDIS_IGNORE_EXCEPTIONS = True

# Elasticsearch connection parameters
ELASTIC_SEARCH_CONFIG = [{
  
  "host": "elasticsearch",
  "port": 9200,
}]

CONTACT_MAILING_ADDRESS = "UNEdx - http://openedx.untic-fibog.com"

DEFAULT_FROM_EMAIL = ENV_TOKENS.get("DEFAULT_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
DEFAULT_FEEDBACK_EMAIL = ENV_TOKENS.get("DEFAULT_FEEDBACK_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
SERVER_EMAIL = ENV_TOKENS.get("SERVER_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
TECH_SUPPORT_EMAIL = ENV_TOKENS.get("TECH_SUPPORT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
CONTACT_EMAIL = ENV_TOKENS.get("CONTACT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
BUGS_EMAIL = ENV_TOKENS.get("BUGS_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
UNIVERSITY_EMAIL = ENV_TOKENS.get("UNIVERSITY_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
PRESS_EMAIL = ENV_TOKENS.get("PRESS_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
PAYMENT_SUPPORT_EMAIL = ENV_TOKENS.get("PAYMENT_SUPPORT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
BULK_EMAIL_DEFAULT_FROM_EMAIL = ENV_TOKENS.get("BULK_EMAIL_DEFAULT_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
API_ACCESS_MANAGER_EMAIL = ENV_TOKENS.get("API_ACCESS_MANAGER_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
API_ACCESS_FROM_EMAIL = ENV_TOKENS.get("API_ACCESS_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])

# Get rid completely of coursewarehistoryextended, as we do not use the CSMH database
INSTALLED_APPS.remove("lms.djangoapps.coursewarehistoryextended")
DATABASE_ROUTERS.remove(
    "openedx.core.lib.django_courseware_routers.StudentModuleHistoryExtendedRouter"
)

# Set uploaded media file path
MEDIA_ROOT = "/openedx/media/"

# Add your MFE and third-party app domains here
CORS_ORIGIN_WHITELIST = []

# Video settings
VIDEO_IMAGE_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT
VIDEO_TRANSCRIPTS_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT

GRADES_DOWNLOAD = {
    "STORAGE_TYPE": "",
    "STORAGE_KWARGS": {
        "base_url": "/media/grades/",
        "location": "/openedx/media/grades",
    },
}

ORA2_FILEUPLOAD_BACKEND = "filesystem"
ORA2_FILEUPLOAD_ROOT = "/openedx/data/ora2"
ORA2_FILEUPLOAD_CACHE_NAME = "ora2-storage"

# Change syslog-based loggers which don't work inside docker containers
LOGGING["handlers"]["local"] = {
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "all.log"),
    "formatter": "standard",
}
LOGGING["handlers"]["tracking"] = {
    "level": "DEBUG",
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "tracking.log"),
    "formatter": "standard",
}
LOGGING["loggers"]["tracking"]["handlers"] = ["console", "local", "tracking"]
# Silence some loggers (note: we must attempt to get rid of these when upgrading from one release to the next)

import warnings
from django.utils.deprecation import RemovedInDjango40Warning, RemovedInDjango41Warning
warnings.filterwarnings("ignore", category=RemovedInDjango40Warning)
warnings.filterwarnings("ignore", category=RemovedInDjango41Warning)
warnings.filterwarnings("ignore", category=DeprecationWarning, module="lms.djangoapps.course_wiki.plugins.markdownedx.wiki_plugin")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="wiki.plugins.links.wiki_plugin")

# Email
EMAIL_USE_SSL = False
# Forward all emails from edX's Automated Communication Engine (ACE) to django.
ACE_ENABLED_CHANNELS = ["django_email"]
ACE_CHANNEL_DEFAULT_EMAIL = "django_email"
ACE_CHANNEL_TRANSACTIONAL_EMAIL = "django_email"
EMAIL_FILE_PATH = "/tmp/openedx/emails"

# Language/locales
LOCALE_PATHS.append("/openedx/locale/contrib/locale")
LOCALE_PATHS.append("/openedx/locale/user/locale")
LANGUAGE_COOKIE_NAME = "openedx-language-preference"

# Allow the platform to include itself in an iframe
X_FRAME_OPTIONS = "SAMEORIGIN"


JWT_AUTH["JWT_ISSUER"] = "http://openedx.untic-fibog.com/oauth2"
JWT_AUTH["JWT_AUDIENCE"] = "openedx"
JWT_AUTH["JWT_SECRET_KEY"] = "KQWwu7sMbuBsqPNbytm3f59p"
JWT_AUTH["JWT_PRIVATE_SIGNING_JWK"] = json.dumps(
    {
        "kid": "openedx",
        "kty": "RSA",
        "e": "AQAB",
        "d": "SyC7snUoeeNu6QCKKs48B8IeZ98m88RsHc6Zwar9wJLf6QBircn8UMRXgz14eUTmXxnIDOfpxw-9oiP6YJbRJLsiZ-2PLSFaZVBJ__BNa98q8rEF_aq3U61_dVFXGYTK-PibwG8x9NgPkLsi0el76noRYYm9Dgng2siMgvGPTx2JzFBHEMMo_v8LUhb5SppFg9jawSrlIFYry4Y67RrBcPZQ7b2haPjeNvaYuzZQ0d901CBgoIPi0f-3-mgYS01XTwZu2UcwDwgmLzqehhp8L9TZ_l2RyfLqXqMZGOCHINgCdPhPXhpA9E0MseTyQ_IdMxtpqtxE5x1Gl4mR99l-XQ",
        "n": "r5WmoCngKEcbQnOwONMYjaI788M-I1V7O_tNtOsJ0IrX3J4P7qkMdr302WotD1q4KniU3ns5iY-UJSJx8sOl7Qp6JqTlFFAiBZ7r7mbDUtJylLUTyPTk5OE2bDxGjyybFjsLw3aEEwaSgWojVLfmSp0kTJZGLNMKqh6arG0dswbPqV2hke_b5Yz1g8oe_t6CPxIxCN_Bczi-3K8baRm4wXWKoD51fbLdJKECYKYRzHmtXF61DWw_ywVrZiUomNx5cQudwrCZhZGqouMPEareXkk89Ux3hCOZ3Hfn_OhlNh2aWQMeXVr2MudC8C-TkmSBOq4B5gIjA6wRJx4vYKiqUw",
        "p": "yZSg_8dlazC6v-xgwtEEY-4j5eOyqLqh0cUsYdhu-vJGRRxAoBV-1Tp0FawsXhu4GR9SNluuRyMye3Nue6Qvl1rz5CaN4rGxRwe7qa_mp8hEPog6WIir3PUcztFugYFNewKrsFsrGM_YLYXqo_V-WUlJmurrbjpbjuARvFL-ko0",
        "q": "3vxrkbpOiSvnWGxVB7fsYpfhbexV6mkSBld-SK2M7LWQvxFGxWAAqJL80gfk6XAJLbOh3wX7ma8p4XHs7eqavNOATE10RJcjIIZfbfT1YGZmjSpoaiFTPr2TZruZg28lVTInriW9ckkniDLaXQPhAqSfZxCnGjNYbTxz23UDaF8",
    }
)
JWT_AUTH["JWT_PUBLIC_SIGNING_JWK_SET"] = json.dumps(
    {
        "keys": [
            {
                "kid": "openedx",
                "kty": "RSA",
                "e": "AQAB",
                "n": "r5WmoCngKEcbQnOwONMYjaI788M-I1V7O_tNtOsJ0IrX3J4P7qkMdr302WotD1q4KniU3ns5iY-UJSJx8sOl7Qp6JqTlFFAiBZ7r7mbDUtJylLUTyPTk5OE2bDxGjyybFjsLw3aEEwaSgWojVLfmSp0kTJZGLNMKqh6arG0dswbPqV2hke_b5Yz1g8oe_t6CPxIxCN_Bczi-3K8baRm4wXWKoD51fbLdJKECYKYRzHmtXF61DWw_ywVrZiUomNx5cQudwrCZhZGqouMPEareXkk89Ux3hCOZ3Hfn_OhlNh2aWQMeXVr2MudC8C-TkmSBOq4B5gIjA6wRJx4vYKiqUw",
            }
        ]
    }
)
JWT_AUTH["JWT_ISSUERS"] = [
    {
        "ISSUER": "http://openedx.untic-fibog.com/oauth2",
        "AUDIENCE": "openedx",
        "SECRET_KEY": "KQWwu7sMbuBsqPNbytm3f59p"
    }
]

# Enable/Disable some features globally
FEATURES["ENABLE_DISCUSSION_SERVICE"] = False
FEATURES["PREVENT_CONCURRENT_LOGINS"] = False

# Disable codejail support
# explicitely configuring python is necessary to prevent unsafe calls
import codejail.jail_code
codejail.jail_code.configure("python", "nonexistingpythonbinary", user=None)
# another configuration entry is required to override prod/dev settings
CODE_JAIL = {
    "python_bin": "nonexistingpythonbinary",
    "user": None,
}

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
VIDEO_IMAGE_SETTINGS["STORAGE_KWARGS"]["location"] = VIDEO_IMAGE_SETTINGS["STORAGE_KWARGS"]["location"].lstrip("/")
VIDEO_TRANSCRIPTS_SETTINGS["STORAGE_KWARGS"]["location"] = VIDEO_TRANSCRIPTS_SETTINGS["STORAGE_KWARGS"]["location"].lstrip("/")
GRADES_DOWNLOAD["STORAGE_KWARGS"]["location"] = GRADES_DOWNLOAD["STORAGE_KWARGS"]["location"].lstrip("/")

# Ora2 setting
ORA2_FILEUPLOAD_BACKEND = "s3"
FILE_UPLOAD_STORAGE_BUCKET_NAME = "openedxuploads"

AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_S3_ENDPOINT_URL = "http://files.openedx.untic-fibog.com"
AWS_AUTO_CREATE_BUCKET = False # explicit is better than implicit
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_EXPIRE = 7 * 24 * 60 * 60  # 1 week: this is necessary to generate valid download urls

# User tasks assets storage
# In theory we could use cms.djangoapps.contentstore.storage.ImportExportS3Storage,
# but this class makes use of boto, which does not support sig3v4 auth.
from storages.backends.s3boto3 import S3Boto3Storage
class MinIOStorage(S3Boto3Storage):  # pylint: disable=abstract-method
    def __init__(self):
        bucket = "openedx"
        super().__init__(bucket=bucket, custom_domain=None, querystring_auth=True)

USER_TASKS_ARTIFACT_STORAGE = f"{__name__}.MinIOStorage"
######## End of settings common to LMS and CMS

######## Common CMS settings

STUDIO_NAME = u"UNEdx - Studio"

# Authentication
SOCIAL_AUTH_EDX_OAUTH2_SECRET = "o1jbau4lLSbpaxva6ud84ujV"
SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT = "http://lms:8000"
SOCIAL_AUTH_REDIRECT_IS_HTTPS = False  # scheme is correctly included in redirect_uri
SESSION_COOKIE_NAME = "studio_session_id"

MAX_ASSET_UPLOAD_FILE_SIZE_IN_MB = 100

FRONTEND_LOGIN_URL = LMS_ROOT_URL + '/login'
FRONTEND_REGISTER_URL = LMS_ROOT_URL + '/register'

# Create folders if necessary
for folder in [LOG_DIR, MEDIA_ROOT, STATIC_ROOT_BASE]:
    if not os.path.exists(folder):
        os.makedirs(folder)

COURSE_IMPORT_EXPORT_STORAGE = USER_TASKS_ARTIFACT_STORAGE

######## End of common CMS settings

# Setup correct webpack configuration file for development
WEBPACK_CONFIG_PATH = "webpack.dev.config.js"

AWS_S3_ENDPOINT_URL = "http://files.openedx.untic-fibog.com:9000"
