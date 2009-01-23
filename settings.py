# -*- coding: utf-8 -*-
# Django settings for mymem project.
from os import path
from django.utils.translation import gettext_lazy as _

DEBUG = True
TEMPLATE_DEBUG = DEBUG

BASEDIR = path.dirname(path.abspath(__file__))

ADMINS = (
    ## ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'djangobile.sqlite'   # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
# although not all variations may be possible on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Madrid'
DATE_FORMAT = 'd/m/Y'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
LANGUAGE_CODE = 'es_ES'

LANGUAGES = (
  ('es', _('Spanish')),
  ('en', _('English')),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = path.join(BASEDIR, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/site_media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend', )

# Make this unique, and don't share it with anybody.
SECRET_KEY = '15=7f)g=)&spodi3bg8%&4fqt%f3rpg%b$-aer5*#a*(rqm79e'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    # This context processor is required to djangobile works properly.
    'djangobile.context_processors.mobile',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    # In order to use request.device in views.
    'djangobile.middleware.DjangoMobileMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    path.join(BASEDIR, 'templates'),
    # In order to use IDEAL language support you must add this template
    # directory.
    path.join(BASEDIR, 'djangobile', 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
)

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

CACHE_DEF_EXPIRE = 60 * 60 * 24

# Absolute path to the CSS's directory that holds media with extended
# capabilities for devices.
# Default: path.join(MEDIA_ROOT, 'css')
IDEAL_CSS_DIR = path.join(MEDIA_ROOT, 'css')

# If you set this to False, the IDEAL language not be processed neither
# rendered, indeed Django will show a TemplateError on IDEAL templates.
IDEAL_LANGUAGE_SUPPORT = False

# IDEAL XMLSchema file against whom IDEAL presentations will be validated.
IDEAL_XML_SCHEMA_FILE = path.join(BASEDIR, 'djangobile', 'transformations',
                                  'cmt.xsd')

# Python WURFL class generated by wurfl2python.py script from pywurfl.
WURFL_CLASS = 'djangobile.wurfl'

# User agent search algorithm.
# Possible values are Tokenizer (default), JaroWinkler and LevenshteinDistance.
# JaroWinkler and LevenshteinDistance require Levenshtein Module >= 0.10.1.
USER_AGENT_SEARCH_ALGORITHM = 'Tokenizer'

# Accuracy value for JaroWinkler search algorithm (0 to 1).
# Default: 0.9
JARO_WINKLER_ACCURACY = 0.9

# List of device capabilities to order template search.
# Default: id, user_agent, fall_back, preferred_markup, model_name, brand_name.
DEVICE_SEARCH_ORDER = (
    'user_agent',
    'brand_name',
)

# If you set this to True, djangobile will print information about device in
# each request through standard output. Useful to debug issues.
# Default: True
DJANGOBILE_SHOW_LOG = True

# Prefix for "extends" and "include" templatetags device aware.
# If None, the native templatetags will be overwritten with
# those where suitable.
# Default: device.
# And its use in templates is such as {% device_extends "template.hmtl" %}
DEVICE_LOADER_TAGS_PREFIX = None

#PREFERRED_MARKUP_ORDER = (
#    'html_web_3_2',
#    'html_web_4_0',
#    'html_wi_imode_compact_generic',
#    'html_wi_imode_html_1',
#    'html_wi_imode_html_2',
#    'html_wi_imode_html_3',
#    'html_wi_imode_html_4',
#    'html_wi_imode_html_5',
#    'html_wi_oma_xhtmlmp_1_0',
#    'html_wi_w3_xhtmlbasic',
#    'wml_1_1',
#    'wml_1_2',
#    'wml_1_3',
#)
