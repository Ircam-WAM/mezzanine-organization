from django.shortcuts import render

from organization.media.models import *
from organization.core.views import *
from dal import autocomplete
from dal_select2_queryset_sequence.views import Select2QuerySetSequenceView
from mezzanine_agenda.models import Event
from organization.magazine.models import Article, Topic, Brief

class VideoListView(ListView):

    model = Video
    template_name='festival/video_list.html'

    def get_queryset(self, **kwargs):
        return self.model.objects.published()

    def get_context_data(self, **kwargs):
        context = super(VideoListView, self).get_context_data(**kwargs)
        context['categories'] = VideoCategory.objects.all()
        return context


class VideoDetailView(SlugMixin, DetailView):

    model = Video
    template_name='festival/video_detail.html'
    context_object_name = 'video'

    def get_context_data(self, **kwargs):
        context = super(VideoDetailView, self).get_context_data(**kwargs)
        return context


class VideoListCategoryView(VideoListView):

    def get_queryset(self):
        self.category = VideoCategory.objects.get(slug=self.kwargs['slug'])
        return self.model.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super(VideoListCategoryView, self).get_context_data(**kwargs)
        context['category'] = self.category
        return context


class MediaListView(ListView):

    template_name='media/media_list.html'
    context_object_name = 'media'

    def get_queryset(self):
        audios = Audio.objects.all()
        videos = Video.objects.all()
        media_list = [video for video in videos]
        media_list += [audio for audio in audios]
        media_list.sort(key=lambda x: x.created_at, reverse=True)

        return media_list
