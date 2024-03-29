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

import json
from datetime import datetime
from dal import autocomplete
from dal_select2_queryset_sequence.views import Select2QuerySetSequenceView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.conf import settings
from organization.media.models import Media, Playlist, PlaylistRelated, LiveStreaming,\
    LIVE_STREAMING_TYPE_CHOICES
from organization.core.views import autocomplete_result_formatting, SlugMixin
from organization.core.utils import split_events_from_other_related_content
from mezzanine.utils.views import paginate
from mezzanine_agenda.models import Event

# temporarily excluse not ready models
EXCLUDED_MODELS = ("organizationplaylist", "personplaylist")


class MediaDetailView(SlugMixin, DetailView):

    model = Media
    context_object_name = 'media'
    template_name = 'media/media/media_detail.html'

    def get_template_names(self):
        templates = super(MediaDetailView, self).get_template_names()
        return templates

    def get_context_data(self, **kwargs):
        context = super(MediaDetailView, self).get_context_data(**kwargs)
        if hasattr(self.object, 'department'):
            if not self.object.department.first() is None:
                department = self.object.department.first().department
                if hasattr(department, 'pages'):
                    if hasattr(department.pages.first(), 'weaving_css_class'):
                        context[
                            'department_weaving_css_class'
                        ] = department.pages.first().weaving_css_class
                        context['department_name'] = department.name
        return context


class PlaylistDetailView(SlugMixin, DetailView):

    model = Playlist
    template_name = 'media/playlist/playlist_detail.html'
    context_object_name = 'playlist'

    def get_context_data(self, **kwargs):
        context = super(PlaylistDetailView, self).get_context_data(**kwargs)
        self.related_objects = []
        self.concrete_objects = []
        related_model = PlaylistRelated._meta.get_fields()
        related_playlist = self.object.playlist_related.all()

        # get dynamically related objects like articleplaylist,
        # projectplaylist, eventplaylist etc....
        for rm in related_model:
            if rm.name not in EXCLUDED_MODELS:
                for rp in related_playlist:
                    if hasattr(rp, rm.name):
                        self.related_objects.append(getattr(rp, rm.name))

        # get dynamically related instance of related objects.
        # Example: articleplaylist => article
        for ro in self.related_objects:
            if not isinstance(ro, int) and ro != self.object:
                for c_field in ro._meta.get_fields():
                    if hasattr(ro, c_field.name):
                        attr = getattr(ro, c_field.name)
                        if not isinstance(attr, int) and\
                                attr != self.object and\
                                not isinstance(attr, PlaylistRelated):
                            self.concrete_objects.append(attr)

        context = split_events_from_other_related_content(
            context,
            self.concrete_objects
        )
        return context


class PlaylistListView(ListView):

    model = Playlist
    template_name = 'media/playlist/playlist_list.html'
    context_object_name = 'playlists'

    def get_queryset(self):
        self.qs = Playlist.objects.all().order_by('-publish_date')
        self.current_type = None
        if "type" in self.kwargs:
            self.qs = self.qs.filter(type=self.kwargs['type'])
            self.current_type = self.kwargs['type']
        return self.qs

    def get_context_data(self, **kwargs):
        context = super(PlaylistListView, self).get_context_data(**kwargs)

        context['playlists'] = paginate(
            self.qs,
            self.request.GET.get("page", 1),
            settings.MEDIA_PER_PAGE,
            settings.MAX_PAGING_LINKS
        )

        context['current_type'] = self.current_type
        return context


class PlayListMediaView(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = Media.objects.all()
        media_title = self.forwarded.get('title', None)
        if media_title:
            qs = qs.filter(title=media_title)
        if self.q:
            qs = qs.filter(title__istartswith=self.q)
        return qs


class MediaOverlayView(SlugMixin, DetailView):

    model = Media
    template_name = 'media/media/media_overlay.html'
    context_object_name = 'media'

    def get_template_names(self):
        templates = super(MediaOverlayView, self).get_template_names()
        templates.insert(
            0,
            'media/' +
            self.object.type.lower() +
            '/'+self.object.type.lower() +
            '_overlay.html'
        )
        return templates


class PlaylistOverlayView(SlugMixin, DetailView):

    model = Playlist
    template_name = 'media/playlist_overlay.html'
    context_object_name = 'playlist'


class LiveStreamingDetailView(SlugMixin, DetailView):

    model = LiveStreaming
    template_name = 'media/live_streaming/live_streaming_detail.html'

    def get_context_data(self, **kwargs):
        context = super(LiveStreamingDetailView, self).get_context_data(**kwargs)

        # check type choices
        type_choices = []
        for st in LIVE_STREAMING_TYPE_CHOICES:
            type_choices.append(st[0])
        if self.kwargs['type'] not in type_choices:
            context['type'] = "html5"
        else:
            context['type'] = self.kwargs['type']

        # slug
        context['slug'] = self.object.slug

        # event data
        all_events = Event.objects.filter(
            location=self.object.event_location
        ).filter(end__gte=datetime.now()).order_by('start')

        events_data = {}
        counter = 0
        for event in all_events:
            events_data[counter] = {}
            events_data[counter]['title'] = event.title
            events_data[counter]['begin'] = event.start.isoformat()
            events_data[counter]['end'] = event.end.isoformat()
            counter += 1

        context['json_event'] = json.dumps(events_data)
        return context


class DynamicMultimediaView(Select2QuerySetSequenceView):

    paginate_by = settings.DAL_MAX_RESULTS

    def get_queryset(self):

        medias = Media.objects.all()
        playlists = Playlist.objects.all()

        if self.q:
            medias = medias.filter(title__icontains=self.q)
            playlists = playlists.filter(title__icontains=self.q)

        qs = autocomplete.QuerySetSequence(medias, playlists, )

        return qs

    def get_results(self, context):
        results = autocomplete_result_formatting(self, context)
        return results
