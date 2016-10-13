from django.shortcuts import render
from collections import defaultdict
from organization.media.models import *
from organization.core.views import *
from dal import autocomplete
from dal_select2_queryset_sequence.views import Select2QuerySetSequenceView


class PlaylistDetailView(SlugMixin, DetailView):

    model = Playlist
    template_name='media/playlist_detail.html'
    context_object_name = 'playlist'

    def get_context_data(self, **kwargs):
        context = super(PlaylistDetailView, self).get_context_data(**kwargs)
        return context


class PlaylistListView(ListView):

    template_name='media/playlist_list.html'
    context_object_name = 'playlists'

    def get_context_data(self, **kwargs):
        context = super(PlaylistListView, self).get_context_data(**kwargs)
        return context

    # def get_queryset(self):
    #     audio_playlists = PlaylistAudio.objects.all()
    #     video_playlists = PlaylistVideo.objects.all()
    #     playlist_list = [video_playlist for video_playlist in video_playlists]
    #     playlist_list += [audio_playlist for audio_playlist in audio_playlists]
    #     playlist_list.sort(key=lambda x: x.created_at, reverse=True)
    #     return playlist_list
