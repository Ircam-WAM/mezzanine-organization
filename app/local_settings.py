import os
from django.utils.translation import ugettext_lazy as _

DEBUG = True if os.environ.get('DEBUG', 'True') else False

# Make these unique, and don't share it with anybody.
SECRET_KEY = "j1qa@u$5ktqr^0_kwh@-j@*-80t$)ht!4-=ybz1xc%@3+r(r&tzefoih"
NEVERCACHE_KEY = "m)u^%r@uh#r3wu0&$=#$1ogx)uy4hv93^2lt%c3@xi=^gifoj8paozijdihazefd"

# DATABASE_ROUTERS = ['eve.routers.EveRouter', 'festival.routers.FestivalRouter',]
# DATABASE_ROUTERS = ['eve.routers.EveRouter',]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': os.environ.get('DB_ENV_POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': '5432',
    },
    'eve': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'eve',
        'USER': 'eve',
        'PASSWORD': 'HmazS2frT',
        'HOST': 'pgdb',
        'PORT': '5432',
    },
}

# DATABASE_ROUTERS = ['eve.routers.EveRouter',]


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

EMAIL_HOST = 'smtp.ircam.fr'
EMAIL_PORT = '25'
DEFAULT_FROM_EMAIL = 'www@ircam.fr'
EMAIL_SUBJECT_PREFIX = "[IRCAM WWW]"

SITE_TITLE = 'IRCAM'
SITE_TAGLINE = 'Institut de Recherche et de Coordination Acoustique et Musique'

SILENCED_SYSTEM_CHECKS = ['fields.W342',]

ADMIN_MENU_ORDER = (
    (_('Content'), ('pages.Page', 'blog.BlogPost', 'mezzanine_agenda.Event',
        'generic.ThreadedComment', (_('Media Library'), 'fb_browse'),)),
    (_("Magazine"), ("magazine.Article",)),
    (_('team'), ('organization.team.Organization', 'organization.team.Team',
        'organization.team.Department', 'organization.team.Person',
        'organization.team.Activity')),
    (_('Projects'), ('organization.project.Project')),
    (_('Festival'), ('organization.festival.Artist', 'organization.festival.Video',
    'organization.festival.Audio', 'organization.festival.Playlist',
    'organization.festival.Featured', 'mezzanine_agenda.EventLocation',
        'mezzanine_agenda.EventCategory', 'mezzanine_agenda.EventPrice',
        'festival.PageCategory',)),
    (_('Users'), ('auth.User', 'auth.Group',)),
    (_('Site'), ('sites.Site', 'redirects.Redirect', 'conf.Setting')),
)

GRAPPELLI_ADMIN_TITLE = 'IRCAM Admin'

SEARCH_MODEL_CHOICES = ()

RATINGS_ACCOUNT_REQUIRED = True

import warnings
warnings.filterwarnings(
        'ignore', r"DateTimeField .* received a naive datetime",
        RuntimeWarning, r'django\.db\.models\.fields')

EVENT_SLUG = 'events'
EVENT_GOOGLE_MAPS_DOMAIN = 'maps.google.fr'
EVENT_PER_PAGE = 50
EVENT_USE_FEATURED_IMAGE = True
EVENT_SHOP_URL = 'http://eve.ircam.fr/manifeste.php/manifestation/'
EVENT_PASS_URL = 'http://eve.ircam.fr/manifeste.php/pass/'

TINYMCE_SETUP_JS = "/srv/app/static/js/tinymce_setup.js"

SLUGIFY = 'django.template.defaultfilters.slugify'

HOME_FEATURED_ID = 1
BREAKING_NEWS_FEATURED_ID = 4

BLOG_POST_PER_PAGE = 200

# The numeric mode to set newly-uploaded files to. The value should be
# a mode you'd pass directly to os.chmod.
FILE_UPLOAD_PERMISSIONS = 0o664
FILE_UPLOAD_TEMP_DIR = '/srv/media/uploads/tmp/'
FILEBROWSER_MAX_UPLOAD_SIZE = 512000000

if DEBUG:
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda x : True
    }
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
