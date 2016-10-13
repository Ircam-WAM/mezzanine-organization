from copy import deepcopy
from django.contrib import admin
from mezzanine.core.admin import *
from organization.media.models import *


class MediaTranscodedAdmin(TabularDynamicInlineAdmin):

    model = MediaTranscoded


class MediaAdmin(BaseTranslationModelAdmin):

    model = Media
    inlines = (MediaTranscodedAdmin,)

class PlaylistMediaInline(TabularDynamicInlineAdmin):

    model = PlaylistMedia


class PlaylistAdmin(BaseTranslationModelAdmin):

    model = Playlist
    inlines = (PlaylistMediaInline,)


class MediaCategoryAdmin(BaseTranslationModelAdmin):

    model = MediaCategory


admin.site.register(Media, MediaAdmin)
admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(MediaCategory, MediaCategoryAdmin)
