from copy import deepcopy
from django.contrib import admin
from mezzanine.core.admin import DisplayableAdmin, OwnableAdmin
from organization.media.models import *


class VideoAdmin(admin.ModelAdmin):

    model = Video


class AudioAdmin(admin.ModelAdmin):

    model = Audio



class PlaylistAdmin(admin.ModelAdmin):

    model = Playlist
    list_display = ('__str__',)
    filter_horizontal = ['audios']


admin.site.register(Video, VideoAdmin)
admin.site.register(Audio, AudioAdmin)
admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(VideoCategory)
