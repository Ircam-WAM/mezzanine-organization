# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Ircam
# Copyright (c) 2016-2017 Guillaume Pellerin
# Copyright (c) 2016-2017 Emilie Zawadzki

# This file is part of mezzanine-organization.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from django.contrib import admin
from mezzanine.core.admin import TabularDynamicInlineAdmin, TeamOwnableAdmin,\
    BaseTranslationModelAdmin
from organization.media.models import MediaTranscoded, MediaImage, Media,\
    PlaylistMedia, Playlist, MediaCategory, LiveStreaming
from organization.media.forms import PlaylistMediaForm
from organization.network.models import MediaDepartment


class MediaTranscodedAdmin(TabularDynamicInlineAdmin):

    model = MediaTranscoded


class MediaImageInline(TabularDynamicInlineAdmin):

    model = MediaImage


class MediaDepartmentInline(TabularDynamicInlineAdmin):

    model = MediaDepartment
    max_num = 1


class MediaAdmin(TeamOwnableAdmin, BaseTranslationModelAdmin):

    model = Media
    inlines = (MediaTranscodedAdmin, MediaImageInline, MediaDepartmentInline)
    list_display = ['title', 'external_id', 'type']
    search_fields = ['title', 'external_id', ]

    def type(self, instance):
        return instance.type


class PlaylistMediaInline(TabularDynamicInlineAdmin):

    model = PlaylistMedia
    form = PlaylistMediaForm


class PlaylistAdmin(BaseTranslationModelAdmin):

    model = Playlist
    inlines = (PlaylistMediaInline,)


class MediaCategoryAdmin(BaseTranslationModelAdmin):

    model = MediaCategory


class LiveStreamingAdmin(BaseTranslationModelAdmin):

    model = LiveStreaming
    list_display = ['title', ]


admin.site.register(Media, MediaAdmin)
admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(MediaCategory, MediaCategoryAdmin)
admin.site.register(LiveStreaming, LiveStreamingAdmin)
