import os
from django.utils.translation import ugettext_lazy as _
from datetime import datetime, date

DEBUG = True if os.environ.get('DEBUG', 'True') else False

# Make these unique, and don't share it with anybody.
SECRET_KEY = "j1qa@u$5ktqr^0_kwh@-j@*-80t$)ht!4-=ybz1xc%@3+r(r&tzefoih"
NEVERCACHE_KEY = "m)u^%r@uh#r3wu0&$=#$1ogx)uy4hv93^2lt%c3@xi=^gifoj8paozijdihazefd"

# DATABASE_ROUTERS = ['eve.routers.EveRouter', 'festival.routers.FestivalRouter',]
DATABASE_ROUTERS = ['eve.routers.EveRouter', 'prestashop.routers.PrestaRouter']

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

if os.environ.get('EVEDB_ENV_POSTGRES_PASSWORD'):
    DATABASES['eve'] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'eve',
        'USER': 'eve',
        'PASSWORD': os.environ.get('EVEDB_ENV_POSTGRES_PASSWORD'),
        'HOST': 'evedb',
        'PORT': '5432',
    }

if os.environ.get('PRESTADB_ENV_MYSQL_PASSWORD'):
    DATABASES['prestashop'] = {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'USER': 'ircam_shops',      # Not used with sqlite3.
        'PASSWORD': os.environ.get('PRESTADB_ENV_MYSQL_PASSWORD'),  # Not used with sqlite3.
        'NAME': 'ircam_shops',
        'HOST': 'prestadb',      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',      # Set to empty string for default. Not used with sqlite3.
        }


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
DEFAULT_TO_EMAIL = 'zawadzki@ircam.fr'
EMAIL_SUBJECT_PREFIX = "[IRCAM WWW]"

SITE_TITLE = 'IRCAM'
SITE_TAGLINE = 'Institut de Recherche et de Coordination Acoustique et Musique'

SILENCED_SYSTEM_CHECKS = ['fields.W342',]

ADMIN_MENU_ORDER = (
    (_('Pages'), ('pages.Page', 'organization-pages.Home',
                 'organization-core.LinkType')),
    (_('Media'), ('organization-media.Media',
                  'organization-media.Playlist',
                 'organization-media.MediaCategory',
                 (_('Media Library'), 'fb_browse'),
                 )),
    (_('Events'), ('mezzanine_agenda.Event',
                  'mezzanine_agenda.EventLocation',
                  'mezzanine_agenda.EventPrice',
                  'mezzanine_agenda.EventCategory',
                  'organization-agenda.EventPublicType',
                  'organization-agenda.EventTrainingLevel',
                  'generic.Keyword',
                  )),
    (_('Magazine'), ('organization-magazine.Article',
                    'organization-magazine.Brief',)),
    (_('Network'), ('organization-network.Organization',
                    'organization-network.Department',
                    'organization-network.Team',
                    'organization-network.Person',
                    'organization-network.Activity',
                    'organization-network.OrganizationType',
                    'organization-network.PersonListBlock',
                    )),
    (_('Activity'), ('organization-network.PersonActivity',
                    'organization-network.ActivityStatus',
                    'organization-network.ActivityGrade',
                    'organization-network.ActivityFramework',
                    'organization-network.ActivityFunction',
                    'organization-network.TrainingType',
                    'organization-network.TrainingTopic',
                    'organization-network.TrainingLevel',
                    'organization-network.TrainingSpeciality',
                    )),
    (_('Projects'), ('organization-projects.Project',
                    'organization-projects.ProjectProgram',
                    'organization-projects.ProjectProgramType',
                    'organization-projects.ProjectTopic',
                    'organization-projects.ProjectProgramType',
                    )),
    (_('Shop'), ('shop.Product',
                    'organization-shop.ProductList',
                    'shop.Order',
                    'shop.DiscountCode',
                    'shop.Sale',
                    )),
    (_('Jobs'), ('organization-job.JobOffer','organization-job.Candidacy')),
    (_('Festival'), ('organization-festival.Artist',)),
    (_('Users'), ('auth.User', 'auth.Group',)),
    (_('Site'), ('sites.Site', 'redirects.Redirect', 'conf.Setting')),
)

DASHBOARD_TAGS = ( ("mezzanine_tags.app_list",), (), ("mezzanine_tags.recent_actions",), )

GRAPPELLI_ADMIN_TITLE = 'IRCAM Admin'

SEARCH_MODEL_CHOICES = ('organization-pages.CustomPage',
                        'organization-network.DepartmentPage',
                        'organization-network.TeamPage',
                        'organization-projects.ProjectTopicPage',
                        'pages.Page',
                        'organization-media.Playlist',
                        'mezzanine_agenda.Event',
                        'organization-projects.Project',
                        'shop.Product')


PAGES_MODELS = ('organization-pages.CustomPage',
                'organization-magazine.Topic',
                'organization-network.DepartmentPage',
                'organization-network.TeamPage',
                'organization-projects.ProjectTopicPage',
                'shop.Product')

SEARCH_PER_PAGE = 10
MAX_PAGING_LINKS = 10

RATINGS_ACCOUNT_REQUIRED = True

import warnings
warnings.filterwarnings(
        'ignore', r"DateTimeField .* received a naive datetime",
        RuntimeWarning, r'django\.db\.models\.fields')

EVENT_SLUG = 'agenda'
EVENT_GOOGLE_MAPS_DOMAIN = 'maps.google.fr'
EVENT_PER_PAGE = 50
EVENT_USE_FEATURED_IMAGE = True
EVENT_SHOP_URL = 'http://eve.ircam.fr/manifeste.php/manifestation/'
EVENT_PASS_URL = 'http://eve.ircam.fr/manifeste.php/pass/'
EVENT_EXCLUDE_TAG_LIST = ['tournees', ]

if DEBUG:
    TINYMCE_SETUP_JS = "/static/js/tinymce_setup.js"
else:
    TINYMCE_SETUP_JS = "/srv/app/organization/core/static/js/tinymce_setup.js"

SLUGIFY = 'django.template.defaultfilters.slugify'

BLOG_POST_PER_PAGE = 200
ARTICLE_PER_PAGE = 4 # just for tests because we haven't got enough content

# The numeric mode to set newly-uploaded files to. The value should be
# a mode you'd pass directly to os.chmod.
FILE_UPLOAD_PERMISSIONS = 0o664
FILE_UPLOAD_TEMP_DIR = '/srv/media/uploads/tmp/'
MAX_UPLOAD_SIZE = 512000000
MAX_UPLOAD_SIZE_FRONT = 10485760
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

GRAPPELLI_INSTALLED = True
# JQUERY_FILENAME = 'jquery-3.1.0.min.js'
JQUERY_UI_FILENAME = 'jquery-ui-1.9.2.min.js'

#SHOP_CURRENCY_LOCALE = ''
SHOP_USE_VARIATIONS = False
SHOP_USE_RATINGS = False

date_now = datetime.now()
CURRENT_SEASON = int(date_now.year) - 1 if datetime(date_now.year, 1,1) <= date_now and date_now <= datetime(date_now.year, 7, 31) else date_now.year
CURRENT_SEASON_STYLED = str(CURRENT_SEASON)[-2:]+"."+str(CURRENT_SEASON+1)[-2:]

PROJECT_DEMOS_DIR = '/srv/media/projects/demos/'
