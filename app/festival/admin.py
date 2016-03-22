from __future__ import unicode_literals

from copy import deepcopy

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from mezzanine_agenda.models import Event, EventLocation
from mezzanine_agenda.admin import *

from mezzanine.conf import settings
from mezzanine.core.admin import DisplayableAdmin, OwnableAdmin

from festival.models import *


class ArtistAdmin(admin.ModelAdmin):

    model = Artist


class VideoAdmin(admin.ModelAdmin):

    model = Video


class VideoAdminDisplayable(DisplayableAdmin):

    fieldsets = deepcopy(VideoAdmin.fieldsets)


class AudioAdmin(admin.ModelAdmin):

    model = Audio


class AudioAdminDisplayable(DisplayableAdmin):

    fieldsets = deepcopy(AudioAdmin.fieldsets)


class ArtistAdminDisplayable(DisplayableAdmin):

    fieldsets = deepcopy(ArtistAdmin.fieldsets)


admin.site.register(PageCategory)
admin.site.register(Artist, ArtistAdminDisplayable)
admin.site.register(Video, VideoAdminDisplayable)
admin.site.register(Audio, AudioAdminDisplayable)
