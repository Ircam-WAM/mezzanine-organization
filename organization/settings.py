# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Ircam
# Copyright (c) 2016-2017 Guillaume Pellerin
# Copyright (c) 2016-2017 Emilie Zawadzki

# This file is part of mezzanine-organization.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from __future__ import absolute_import, unicode_literals

import os
import ldap
import logging
import warnings
from datetime import date
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType

DEBUG = True if os.environ.get('DEBUG') == 'True' else False

warnings.filterwarnings(
        'ignore', r"DateTimeField .* received a naive datetime",
        RuntimeWarning, r'django\.db\.models\.fields')

SILENCED_SYSTEM_CHECKS = ['fields.W342', ]

######################
# MEZZANINE SETTINGS #
######################

# The following settings are already defined with default values in
# the ``defaults.py`` module within each of Mezzanine's apps, but are
# common enough to be put here, commented out, for conveniently
# overriding. Please consult the settings documentation for a full list
# of settings Mezzanine implements:
# http://mezzanine.jupo.org/docs/configuration.html#default-settings

# Controls the ordering and grouping of the admin menu.
#
# ADMIN_MENU_ORDER = (
#     ("Content", ("pages.Page", "blog.BlogPost",
#        "generic.ThreadedComment", (_("Media Library"), "fb_browse"),)),
#     (_("Shop"), ("shop.Product", "shop.ProductOption", "shop.DiscountCode",
#        "shop.Sale", "shop.Order")),
#     ("Site", ("sites.Site", "redirects.Redirect", "conf.Setting")),
#     ("Users", ("auth.User", "auth.Group",)),
# )

# A three item sequence, each containing a sequence of template tags
# used to render the admin dashboard.
#
# DASHBOARD_TAGS = (
#     ("blog_tags.quick_blog", "mezzanine_tags.app_list"),
#     ("comment_tags.recent_comments",),
#     ("mezzanine_tags.recent_actions",),
# )

# A sequence of templates used by the ``page_menu`` template tag. Each
# item in the sequence is a three item sequence, containing a unique ID
# for the template, a label for the template, and the template path.
# These templates are then available for selection when editing which
# menus a page should appear in. Note that if a menu template is used
# that doesn't appear in this setting, all pages will appear in it.

PAGE_MENU_TEMPLATES = (
    (1, _("Header"), "pages/menus/action.html"),
    (2, _("Menu"), "pages/menus/header.html"),
    (3, _("Footer vertical"), "pages/menus/footer_vertical.html"),
    (4, _("Footer horizontal"), "pages/menus/footer_horizontal.html"),
    (5, _("Magazine"), "pages/menus/magazine.html"),
    (6, _("Vous êtes"), "pages/menus/vous_etes.html"),
    (7, _("Personnes"), "pages/menus/tree.html"),
    (8, _("Candidacies"), "pages/menus/candidacies.html"),
)

PAGE_MENU_TEMPLATES_DEFAULT = ()

MENU_PERSON_ID = 7

# A sequence of fields that will be injected into Mezzanine's (or any
# library's) models. Each item in the sequence is a four item sequence.
# The first two items are the dotted path to the model and its field
# name to be added, and the dotted path to the field class to use for
# the field. The third and fourth items are a sequence of positional
# args and a dictionary of keyword args, to use when creating the
# field instance. When specifying the field class, the path
# ``django.models.db.`` can be omitted for regular Django model fields.
#

# EXTRA_MODEL_FIELDS = (
#  )

EXTRA_MODEL_FIELDS = (
    )

# Setting to turn on featured images for blog posts. Defaults to False.
#
BLOG_USE_FEATURED_IMAGE = True

# If True, the django-modeltranslation will be added to the
# INSTALLED_APPS setting.
USE_MODELTRANSLATION = True

# SEARCH_MODEL_CHOICES = ('shop.Product',)

COMMENTS_ACCOUNT_REQUIRED = True
RATINGS_ACCOUNT_REQUIRED = True

########################
# MAIN DJANGO SETTINGS #
########################

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Paris'

# If you set this to True, Django will use timezone-aware datetimes.
USE_TZ = True

# Whether a user's session cookie expires when the Web browser is closed.
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

SITE_ID = 1

MULTIPLE_DOMAIN_SETTING_ALLOWED = True

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
USE_L10N = True

AUTHENTICATION_BACKENDS = (
    "mezzanine.core.auth_backends.MezzanineBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
    "guardian.backends.ObjectPermissionBackend",
)

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

#########
# PATHS #
#########

# Full filesystem path to the project.
PROJECT_APP_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_APP = os.path.basename(PROJECT_APP_PATH)
PROJECT_ROOT = BASE_DIR = os.path.dirname(PROJECT_APP_PATH)

# Every cache key will get prefixed with this value - here we set it to
# the name of the directory the project is in to try and use something
# project specific.
CACHE_MIDDLEWARE_KEY_PREFIX = PROJECT_APP

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/static/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
# STATIC_ROOT = os.path.join(PROJECT_ROOT, STATIC_URL.strip("/"))
STATIC_ROOT = '/srv/static/'

STATIC_HASH = os.environ.get('STATIC_HASH')\
    if os.environ.get('STATIC_HASH') is not None else ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = "/media/"

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
# MEDIA_ROOT = os.path.join(PROJECT_ROOT, *MEDIA_URL.strip("/").split("/"))
MEDIA_ROOT = '/srv/media/'

# Package/module name to import the root urlpatterns from for the project.
ROOT_URLCONF = "urls"

#########
# LOCALE #
#########

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "fr"

# Supported languages
LANGUAGES = (
    ('fr', _('French')),
    ('en', _('English')),
)
LOCALE_PATHS = (
    os.path.join(PROJECT_ROOT, 'organization/locale'),
)
# print("LOCALE_PATHS", LOCALE_PATHS)
#############
# DATABASES #
#############

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': os.environ.get('DB_ENV_POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': '5432',
    },
}


################
# APPLICATIONS #
################

INSTALLED_APPS = [
    # the current theme has to be defined in main local_settings as HOST_THEMES
    # 'ircam_www_theme',
    "modeltranslation",
    "dal_legacy_static",
    "dal",
    "dal_queryset_sequence",
    "dal_select2",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.redirects",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django.contrib.messages",
    'django_extensions',
    "mezzanine.boot",
    "mezzanine.conf",
    "mezzanine.core",
    "mezzanine.generic",
    "mezzanine.pages",
    "mezzanine.blog",
    "mezzanine.forms",
    "mezzanine.twitter",
    "mezzanine.accounts",
    # "mezzanine.galleries",
    # "mezzanine.mobile",
    "cartridge.shop",
    # 'djangobower',
    "meta",
    "mezzanine_agenda",
    "organization.core",
    "organization.media",
    "organization.pages",
    "organization.network",
    "organization.magazine",
    "organization.projects",
    "organization.agenda",
    "organization.shop",
    "organization.job",
    "organization.utils",
    # "sorl.thumbnail", # required for thumbnail support
    'hijack',
    'compat',
    'guardian',
    'extra_views',
]

BOWER_COMPONENTS_ROOT = '/srv/bower/'
BOWER_PATH = '/usr/local/bin/bower'
BOWER_INSTALLED_APPS = (
    'jquery#2.2.4',
    'font-awesome#4.4.0',
)

# Add Migration Module path see : https://github.com/stephenmcd/mezzanine/blob/master/docs/model-customization.rst#field-injection-caveats  # noqa: E501
MIGRATION_MODULES = {
    "blog": "mezzanine.migrations.blog",
    "forms": "mezzanine.migrations.forms",
    "galleries": "mezzanine.migrations.galleries",
    "pages": "mezzanine.migrations.pages",
    "conf": "mezzanine.migrations.conf",
    "shop": "mezzanine.migrations.shop",
    "generic": "mezzanine.migrations.generic",
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'context_processors': (
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.static',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.tz',
                'mezzanine.conf.context_processors.settings',
                'mezzanine.pages.context_processors.page',
                'organization.core.context_processors.organization_settings',
                'organization.utils.context_processors.static_hash'
            ),
            'loaders': [
                'mezzanine.template.loaders.host_themes.Loader',
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        }
    }
]

# List of middleware classes to use. Order is important; in the request phase,
# these middleware classes will be applied in the order given, and in the
# response phase the middleware will be applied in reverse order.
MIDDLEWARE = (
    # 'sandbox.middleware.StartupMiddleware',
    "mezzanine.core.middleware.UpdateCacheMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    # Uncomment if using internationalisation or localisation
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "mezzanine.core.request.CurrentRequestMiddleware",
    "mezzanine.core.middleware.RedirectFallbackMiddleware",
    "mezzanine.core.middleware.AdminLoginInterfaceSelectorMiddleware",
    "mezzanine.core.middleware.SitePermissionMiddleware",
    # Uncomment the following if using any of the SSL settings:
    # "mezzanine.core.middleware.SSLRedirectMiddleware",
    "mezzanine.pages.middleware.PageMiddleware",
    # "mezzanine.core.middleware.FetchFromCacheMiddleware",
    "cartridge.shop.middleware.ShopMiddleware",
)

# Store these package names here as they may change in the future since
# at the moment we are using custom forks of them.
PACKAGE_NAME_FILEBROWSER = "filebrowser_safe"
PACKAGE_NAME_GRAPPELLI = "grappelli_safe"

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
    # 'djangobower.finders.BowerFinder',
)

GRAPH_MODELS = {
  'all_applications': True,
  'group_models': True,
}

SLUGIFY = 'django.template.defaultfilters.slugify'


########
# DRUM #
########

# Drum-specific Mezzanine settings
# ACCOUNTS_PROFILE_MODEL = "links.Profile"
# SITE_TITLE = "IRCAM"
RATINGS_RANGE = (-1, 1)
COMMENTS_ACCOUNT_REQUIRED = True
RATINGS_ACCOUNT_REQUIRED = True
ACCOUNTS_PROFILE_VIEWS_ENABLED = False
# SEARCH_MODEL_CHOICES = ("links.Link",)

# Drum settings
ALLOWED_DUPLICATE_LINK_HOURS = 24 * 7 * 3
ITEMS_PER_PAGE = 20
LINK_REQUIRED = False
AUTO_TAG = True

#########################
# FILE BROWSER          #
#########################

# The numeric mode to set newly-uploaded files to. The value should be
# a mode you'd pass directly to os.chmod.
FILE_UPLOAD_PERMISSIONS = 0o664
FILE_UPLOAD_TEMP_DIR = '/srv/media/uploads/tmp/'
if not os.path.exists(FILE_UPLOAD_TEMP_DIR):
    os.makedirs(FILE_UPLOAD_TEMP_DIR)

MAX_UPLOAD_SIZE = 512000000
MAX_UPLOAD_SIZE_FRONT = 10485760
FILEBROWSER_MAX_UPLOAD_SIZE = 512000000

THUMBNAILS_DIR_NAME = 'thumbs'

# EXTENSIONS AND FORMATS
# Allowed Extensions for File Upload. Lower case is important.
FILEBROWSER_EXTENSIONS = {
    'Folder': [''],
    'Image': ['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff'],
    'Document': ['.pdf', '.doc', '.rtf', '.txt', '.xls', '.csv', '.docx'],
    'Video': ['.mov', '.wmv', '.mpeg', '.mpg', '.avi', '.rm'],
    'Audio': ['.mp3', '.mp4', '.wav', '.aiff', '.midi', '.m4p']
    }


# Define different formats for allowed selections.
# This has to be a subset of EXTENSIONS.
# e.g., add ?type=image to the browse-URL ...
FILEBROWSER_SELECT_FORMATS = {
    'File': ['Folder', 'Document'],
    'Image': ['Image'],
    'Media': ['Video', 'Audio'],
    'Audio': ['Audio'],
    'Document': ['Document'],
    # for TinyMCE we can also define lower-case items
    'image': ['Image'],
    'file': ['Folder', 'Image', 'Document'],
    'media': ['Video', 'Audio'],
    'audio': ['Audio'],
}


#########################
# ADMIN MENU            #
#########################

GRAPPELLI_INSTALLED = True
JQUERY_FILENAME = 'jquery-3.1.0.min.js'
JQUERY_UI_FILENAME = 'jquery-ui-1.12.1.min.js'
TINYMCE_SETUP_JS = "js/tinymce_setup.js"

ADMIN_MENU_ORDER = (
    (_('Pages'), ('pages.Page', 'organization_pages.Home',
                 'organization_core.LinkType')),
    (_('Media'), ('organization_media.Media',
                  'organization_media.Playlist',
                  'organization_media.LiveStreaming',
                  'organization_media.MediaCategory',
                 (_('Media Library'), 'fb_browse'),
                 )),
    (_('Events'), ('mezzanine_agenda.Event',
                  'mezzanine_agenda.Season',
                  'mezzanine_agenda.EventLocation',
                  'mezzanine_agenda.EventShop',
                  'mezzanine_agenda.EventPrice',
                  'mezzanine_agenda.EventCategory',
                  'organization_agenda.EventPublicType',
                  'organization_agenda.EventTrainingLevel',
                  'generic.Keyword',
                  )),
    (_('Magazine'), ('organization_magazine.Article',
                    'organization_magazine.Brief',)),
    (_('Network'), ('organization_network.Organization',
                    'organization_network.OrganizationLinked',
                    'organization_network.OrganizationRole',
                    'organization_network.OrganizationType',
                    'organization_network.Department',
                    'organization_network.Team',
                    'organization_network.Person',
                    'organization_network.Activity',
                    'organization_network.PersonListBlock',
                    )),
    (_('Activity'), ('organization_network.PersonActivity',
                    'organization_network.ActivityStatusFamily',
                    'organization_network.ActivityStatus',
                    'organization_network.ActivityGrade',
                    'organization_network.ActivityFramework',
                    'organization_network.ActivityFunction',
                    'organization_network.ProjectActivity',
                    'organization_network.TrainingType',
                    'organization_network.TrainingTopic',
                    'organization_network.TrainingLevel',
                    'organization_network.TrainingSpeciality',
                    )),
    (_('Timesheet'), ('organization_network.ActivityWeeklyHourVolume',
                     'organization_network.PersonActivityTimeSheet'
                    )),
    (_('Projects'), ('organization_projects.Project',
                    'organization_projects.ProjectCall',
                    'organization_projects.ProjectContact',
                    'organization_projects.ProjectProgram',
                    'organization_projects.ProjectProgramType',
                    'organization_projects.ProjectTopic',
                    'organization_projects.ProjectWorkPackage',
                    'organization_projects.ProjectPublicData',
                    'organization_projects.ProjectPrivateData',
                    'organization_projects.ProjectResidency',
                    'organization_projects.Repository',
                    'organization_projects.RepositorySystem',
                    'organization_projects.ProjectDemo',
                    )),
    (_('Shop'), ('shop.Product',
                    'organization-shop.ProductList',
                    'shop.Order',
                    'shop.DiscountCode',
                    'shop.Sale',
                    )),
    (_('Jobs'), ('organization_job.JobOffer','organization_job.Candidacy')),
    (_('Users'), ('auth.User', 'auth.Group',)),
    (_('Site'), ('sites.Site', 'redirects.Redirect', 'conf.Setting')),
)

DASHBOARD_TAGS = (
    (
        "mezzanine_tags.app_list",
    ),
    (),
    (
        "mezzanine_tags.recent_actions",
    ),
)

SEARCH_MODEL_CHOICES = ('organization_pages.CustomPage',
                        'organization_network.DepartmentPage',
                        'organization_network.TeamPage',
                        'organization_network.Person',
                        'organization_projects.ProjectTopicPage',
                        'pages.Page',
                        'organization_media.Playlist',
                        'mezzanine_agenda.Event',
                        'organization_projects.ProjectPage',
                        'shop.Product',
                        'organization_magazine.Article')

# authorize models which does not heritate from Displayable
SEARCH_MODEL_NO_DISPLAYABLE = ('organization_network.Person',)

PAGES_MODELS = ('organization_pages.CustomPage',
                'organization_magazine.Topic',
                'organization_network.DepartmentPage',
                'organization_network.TeamPage',
                'organization_projects.ProjectTopicPage',
                'shop.Product')

SEARCH_PARENTS_MODELS = ('organization_network.Person',)

PAGES_PUBLISHED_INCLUDE_LOGIN_REQUIRED = True

SEARCH_PER_PAGE = 10
MAX_PAGING_LINKS = 10
DAL_MAX_RESULTS = 100

# EVENTS

EVENT_SLUG = 'agenda'
EVENT_GOOGLE_MAPS_DOMAIN = 'www.google.com'
EVENT_PER_PAGE = 50
EVENT_USE_FEATURED_IMAGE = True
EVENT_EXCLUDE_TAG_LIST = []
EVENT_TAG_HIGHLIGHTED = 2
PAST_EVENTS = True

# SEASON
# year is dynamic in context processor

SEASON_START_MONTH = 7
SEASON_START_DAY = 31
SEASON_END_MONTH = 8
SEASON_END_DAY = 1

TEAM_HOMEPAGE_ITEM = 9

BLOG_SLUG = 'article'
BLOG_POST_PER_PAGE = 200
ARTICLE_PER_PAGE = 10
MEDIA_PER_PAGE = 9

# SHOP_CURRENCY_LOCALE = ''
SHOP_USE_VARIATIONS = False
SHOP_USE_RATINGS = False

PROJECT_DEMOS_DIR = '/srv/media/projects/demos/'

if not os.path.exists(PROJECT_DEMOS_DIR):
    os.makedirs(PROJECT_DEMOS_DIR)

FORMAT_MODULE_PATH = [
    'organization.formats',
]


#########################
# OPTIONAL APPLICATIONS #
#########################

# These will be added to ``INSTALLED_APPS``, only if available.
OPTIONAL_APPS = (
    "django_extensions",
    "compressor",
    PACKAGE_NAME_FILEBROWSER,
    PACKAGE_NAME_GRAPPELLI,
)

if DEBUG:
    OPTIONAL_APPS += ('debug_toolbar', )  # , 'hijack_admin',)
    MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

INTERNAL_IPS = ['127.0.0.1', '172.17.0.1', '172.17.0.2']

DEBUG_TOOLBAR_PATCH_SETTINGS = False
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

# HIJACK
HIJACK_DISPLAY_WARNING = False
HIJACK_ALLOW_GET_REQUESTS = False
HIJACK_REGISTER_ADMIN = False
# SILENCED_SYSTEM_CHECKS = ["hijack_admin.E001"]

if DEBUG:
    SILENCED_SYSTEM_CHECKS = []
    HIJACK_LOGIN_REDIRECT_URL = "/person"
    HIJACK_LOGOUT_REDIRECT_URL = "/"
    HIJACK_ALLOW_GET_REQUESTS = True
    HIJACK_DISPLAY_WARNING = True
    HIJACK_REGISTER_ADMIN = True

##############################################
#           AUTHENTIFICATION LDAP            #
##############################################
# You can use LDAP Authentication by using 'Django Auth LDAP'#

# 1 - Activate logging :
# logging
if DEBUG:
    logger = logging.getLogger('django_auth_ldap')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)

# 2 - Specify your LDAP settings :
AUTH_LDAP_SERVER_URI = "ldap://clusterldap1.ircam.fr"
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    "ou=People,dc=ircam,dc=fr",
    ldap.SCOPE_SUBTREE,
    "(uid=%(user)s)"
)

# Set up the basic group parameters.
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
    "ou=People,dc=ircam,dc=fr",
    ldap.SCOPE_SUBTREE,
    "(objectClass=groupOfNames)"
)
AUTH_LDAP_GROUP_TYPE = GroupOfNamesType(name_attr="cn")

# Populate the Django user from the LDAP directory.
AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail"
}

# This is the default, but I like to be explicit.
AUTH_LDAP_ALWAYS_UPDATE_USER = True

# Use LDAP group membership to calculate group permissions.
AUTH_LDAP_FIND_GROUP_PERMS = True

# Cache group memberships for an hour to minimize LDAP traffic
AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 3600

##################
#    GUARDIAN    #
##################

ANONYMOUS_USER_NAME = None
LOGIN_REDIRECT_URL = reverse_lazy('organization_network-person-detail')

# Themes
# HOST_THEMES = [
#     ('example.com', 'ircam_www_theme'),
# ]

# TIMESHEET
TIMESHEET_USER_TEST = 1
TIMESHEET_LOG_PATH = "/var/log/cron/"
TIMESHEET_START = date(2015, 1, 1)  # arbitrary timesheet start due to missing data
IRCAM_EMPLOYER = 1
if DEBUG:
    TIMESHEET_MASTER_MAIL = "foo@bar.fr"
    TIMESHEET_BCC_MAIL = "de@bug.com"
else:
    TIMESHEET_MASTER_MAIL = "foo@bar.fr"
    TIMESHEET_BCC_MAIL = "de@bug.com"

# HAL

HAL_URL = "//haltools.archives-ouvertes.fr/Public/afficheRequetePubli.php?" \
    "affi_exp=Ircam&CB_auteur=oui&CB_titre=oui" \
    "&CB_article=oui&langue=Anglais&tri_exp=annee_publi&tri_exp2=typdoc&"\
    "tri_exp3=date_publi&ordre_aff=TA&Fen=Aff&Formate=Oui"

HAL_LABOS_EXP = "labos_exp="
HAL_URL_CSS = "&css=//%s/static/css/index.min.css"
HAL_LIMIT_PUB = "&NbAffiche="
HAL_YEAR_BEGIN = 1977

# Ownable
OWNABLE_MODELS_ALL_EDITABLE = []

# ARTICLE LIST
ARTICLE_KEYWORDS = ['', ]

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

# OAUTH2
OAUTH2_IRCAM = True
if OAUTH2_IRCAM is not True:
    LOGIN_URL = '/accounts/login'
else:
    LOGIN_URL = '/accounts/ircamauth/login/'
OAUTH_SERVER_BASEURL = os.getenv('OAUTH_SERVER_BASEURL')
USER_SERVER_BASEURL = os.getenv('USER_SERVER_BASEURL')

LOGOUT_URL = '/accounts/logout/'
LOGIN_REDIRECT_URL = '/person/'
# LOGIN_REDIRECT_URL = '/dashboard/'
# Account creation URL
OAUTH_SIGNUP_URL = '{}/accounts/signup'.format(USER_SERVER_BASEURL)
# Creation of an internal user's group for OAUTH2/LDAP and
# Dashboard presentation (internal/external user)
ORGANIZATION_INTERN_USERS_GROUP = 'Ircam - Intern'
