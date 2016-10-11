from copy import deepcopy
from django.contrib import admin
from mezzanine.core.admin import *
from organization.media.models import *


class VideoAdmin(BaseTranslationModelAdmin):

    model = Video


class AudioAdmin(BaseTranslationModelAdmin):

    model = Audio


class PlaylistAdmin(BaseTranslationModelAdmin):

    model = Playlist
    list_display = ('__str__',)
    filter_horizontal = ['audios']


class MediaCategoryAdmin(BaseTranslationModelAdmin):

    model = MediaCategory


admin.site.register(Video, VideoAdmin)
admin.site.register(Audio, AudioAdmin)
admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(MediaCategory, MediaCategoryAdmin)
