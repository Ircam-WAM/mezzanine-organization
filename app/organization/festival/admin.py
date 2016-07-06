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


class VideoAdmin(admin.ModelAdmin):

    model = Video


class VideoAdminDisplayable(DisplayableAdmin):

    fieldsets = deepcopy(VideoAdmin.fieldsets)
    filter_horizontal = ['artists']


class AudioAdmin(admin.ModelAdmin):

    model = Audio


class AudioAdminDisplayable(DisplayableAdmin):

    fieldsets = deepcopy(AudioAdmin.fieldsets)
    filter_horizontal = ['artists']


class ArtistAdminDisplayable(DisplayableAdmin):

    fieldsets = deepcopy(ArtistAdmin.fieldsets)


class PlaylistAdmin(admin.ModelAdmin):

    model = Playlist
    list_display = ('__unicode__',)
    filter_horizontal = ['audios']


class FeaturedAdmin(admin.ModelAdmin):

    model = Featured
    list_display = ('__unicode__',)
    filter_horizontal = ['artists', 'events', 'videos', 'pages', 'blogposts', 'pages', 'playlists']


admin.site.register(Artist, ArtistAdminDisplayable)
admin.site.register(Video, VideoAdminDisplayable)
admin.site.register(Audio, AudioAdminDisplayable)
admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(Featured, FeaturedAdmin)
admin.site.register(VideoCategory)
