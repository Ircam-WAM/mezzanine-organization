from __future__ import unicode_literals

from copy import deepcopy

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from mezzanine_agenda.models import Event, EventLocation
from mezzanine_agenda.admin import *

from mezzanine.conf import settings
from mezzanine.core.admin import DisplayableAdmin, OwnableAdmin

from festival.models import *


class FestivalEventInline(admin.StackedInline):
    model = FestivalEvent
    extra = 1


class FestivalEventAdmin(EventAdmin):

    inlines = [FestivalEventInline, ]


class ArtistAdmin(admin.ModelAdmin):

    model = Artist


class VideoAdmin(admin.ModelAdmin):

    model = Video


class VideoAdminDisplayable(DisplayableAdmin):

    fieldsets = deepcopy(VideoAdmin.fieldsets)


class ArtistAdminDisplayable(DisplayableAdmin):

    fieldsets = deepcopy(ArtistAdmin.fieldsets)


admin.site.unregister(Event)
admin.site.register(Event, FestivalEventAdmin)

admin.site.register(Artist, ArtistAdminDisplayable)
admin.site.register(Video, VideoAdminDisplayable)
