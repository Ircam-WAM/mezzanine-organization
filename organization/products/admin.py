from copy import deepcopy

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.admin import *

from organization.projects.models import *
from organization.pages.models import *
from organization.media.models import Video, Audio
