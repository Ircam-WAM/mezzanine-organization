from django.shortcuts import render
from django.views.generic import *
from django.views.generic.base import *
from django.shortcuts import get_object_or_404

from organization.festival.models import *
from mezzanine_agenda.models import EventLocation

from organization.core.views import *


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
