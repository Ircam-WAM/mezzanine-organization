from django.shortcuts import render
from django.views.generic import *
from django.views.generic.base import *
from django.shortcuts import get_object_or_404

from organization.festival.models import *
from mezzanine_agenda.models import EventLocation


class SlugMixin(object):

    def get_object(self):
        objects = self.model.objects.all()
        return get_object_or_404(objects, slug=self.kwargs['slug'])


class ArtistListView(ListView):

    model = Artist
    template_name='festival/artist_list.html'

    def get_queryset(self, **kwargs):
        return self.model.objects.published()

    def get_context_data(self, **kwargs):
        context = super(ArtistListView, self).get_context_data(**kwargs)
        return context


class ArtistDetailView(SlugMixin, DetailView):

    model = Artist
    template_name='festival/artist_detail.html'
    context_object_name = 'artist'

    def get_context_data(self, **kwargs):
        context = super(ArtistDetailView, self).get_context_data(**kwargs)
        return context


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
