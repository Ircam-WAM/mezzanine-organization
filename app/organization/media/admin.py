from copy import deepcopy
from django.contrib import admin
from mezzanine.core.admin import DisplayableAdmin, OwnableAdmin
from organization.media.models import *


class VideoAdmin(admin.ModelAdmin):

    model = Video


class VideoAdminDisplayable(DisplayableAdmin):

    fieldsets = deepcopy(VideoAdmin.fieldsets)
    #filter_horizontal = ['artists']


class AudioAdmin(admin.ModelAdmin):

    model = Audio


class AudioAdminDisplayable(DisplayableAdmin):

    fieldsets = deepcopy(AudioAdmin.fieldsets)
    # filter_horizontal = ['artists']


class PlaylistAdmin(admin.ModelAdmin):

    model = Playlist
    list_display = ('__str__',)
    filter_horizontal = ['audios']


admin.site.register(Video, VideoAdminDisplayable)
admin.site.register(Audio, AudioAdminDisplayable)
admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(VideoCategory)
