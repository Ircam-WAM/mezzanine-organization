from django.shortcuts import render
from collections import defaultdict
from organization.media.models import *
from organization.core.views import *
from dal import autocomplete
from dal_select2_queryset_sequence.views import Select2QuerySetSequenceView
from django.core.exceptions import FieldDoesNotExist


class PlaylistDetailView(SlugMixin, DetailView):

    model = Playlist
    template_name='media/playlist_detail.html'
    context_object_name = 'playlist'
    
    def get_context_data(self, **kwargs):
        self.related_objects = []
        context = super(PlaylistDetailView, self).get_context_data(**kwargs)
        related_model = PlaylistRelated._meta.get_fields()
        related_playlist = self.object.playlist_related.all()
        for rm in related_model:
            for rp in related_playlist:
                if hasattr(rp, rm.name):
                    self.related_objects.append(getattr(rp, rm.name))

        context['related_objects'] = self.related_objects
        return context


class PlaylistListView(ListView):

    model = Playlist
    template_name='media/playlist_list.html'
    context_object_name = 'playlists'
    def get_queryset(self):
        qs = Playlist.objects.all()
        self.current_type = None
        if "type" in self.kwargs:
            qs = qs.filter(type=self.kwargs['type'])
            self.current_type = self.kwargs['type']
        return qs
    def get_context_data(self, **kwargs):
        context = super(PlaylistListView, self).get_context_data(**kwargs)
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


class MediaDetailView(SlugMixin, DetailView):

    model = Media
    template_name='media/media_detail.html'
    context_object_name = 'media'
