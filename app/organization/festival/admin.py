from __future__ import unicode_literals

from copy import deepcopy

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from mezzanine_agenda.models import Event, EventLocation
from mezzanine_agenda.admin import *

from mezzanine.conf import settings
from mezzanine.core.admin import DisplayableAdmin, OwnableAdmin

from organization.festival.models import *


class ArtistAdmin(admin.ModelAdmin):

    model = Artist


class ArtistAdminDisplayable(DisplayableAdmin):

    fieldsets = deepcopy(ArtistAdmin.fieldsets)


# admin.site.register(Artist, ArtistAdminDisplayable)
