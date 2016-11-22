from django.shortcuts import render
from collections import defaultdict
from organization.media.models import *
from organization.core.views import *
from dal import autocomplete
from dal_select2_queryset_sequence.views import Select2QuerySetSequenceView
from django.core.exceptions import FieldDoesNotExist

# temporarily excluse not ready models
EXCLUDED_MODELS = ("organizationplaylist", "personplaylist")


class MediaDetailView(SlugMixin, DetailView):

    model = Media
    template_name='media/media_detail.html'


class PlaylistDetailView(SlugMixin, DetailView):

    model = Playlist
    template_name='media/playlist_detail.html'
    context_object_name = 'playlist'
    def get_context_data(self, **kwargs):
        context = super(PlaylistDetailView, self).get_context_data(**kwargs)
        self.related_objects = []
        self.concrete_objects = []
        related_model = PlaylistRelated._meta.get_fields()
        related_playlist = self.object.playlist_related.all()

        # get dynamically related objects like articleplaylist, projectplaylist, eventplaylist etc....
        for rm in related_model:
            if rm.name not in EXCLUDED_MODELS :
                for rp in related_playlist:
                    if hasattr(rp, rm.name):
                        self.related_objects.append(getattr(rp, rm.name))

        # get dynamically related instance of related objects. Example: articleplaylist => article
        for ro in self.related_objects:
            if not isinstance(ro, int) and ro != self.object:
                for c_field in ro._meta.get_fields():
                    if hasattr(ro, c_field.name):
                        attr = getattr(ro, c_field.name)
                        if not isinstance(attr, int) and attr != self.object and not isinstance(attr, PlaylistRelated):
                            self.concrete_objects.append(attr)

        context['concrete_objects'] = self.concrete_objects
        return context


class PlaylistListView(ListView):

    model = Playlist
    template_name='media/playlist_list.html'
    context_object_name = 'playlists'
    def get_queryset(self):
        self.qs = Playlist.objects.all()
        self.current_type = None
        if "type" in self.kwargs:
            self.qs = self.qs.filter(type=self.kwargs['type'])
            self.current_type = self.kwargs['type']
        return self.qs
    def get_context_data(self, **kwargs):
        context = super(PlaylistListView, self).get_context_data(**kwargs)

        context['playlists'] = paginate(self.qs, self.request.GET.get("page", 1),
                          settings.MEDIA_PER_PAGE,
                          settings.MAX_PAGING_LINKS)

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
