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

from cartridge.shop.models import Product
from dal import autocomplete
from dal_select2_queryset_sequence.views import Select2QuerySetSequenceView
from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView
from django.urls import reverse_lazy
from mezzanine.conf import settings
from organization.pages.models import CustomPage, ExtendedCustomPage
from organization.core.views import SlugMixin, autocomplete_result_formatting
from organization.magazine.models import Article, Brief
from organization.pages.models import Home
from organization.pages.forms import YearForm
from organization.agenda.models import Event
from organization.media.models import Playlist, Media
from organization.network.models import Person, Organization
from organization.projects.models import Project, ProjectPage
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from queryset_sequence import QuerySetSequence


class HomeView(SlugMixin, DetailView):

    model = Home
    template_name = 'index.html'
    context_object_name = 'home'

    def get_object(self, **kwargs):
        homes = self.model.objects.published()
        if homes:
            return homes.latest("publish_date")
        return None

    def get_single_body(self, model_type):
        for body in self.bodys:
            if body.content_type:
                if body.content_type.model == model_type:
                    return body.content_object
        return

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['briefs'] = Brief.objects.published().order_by('-publish_date')[:8]
        try:
            from mezzanine_agenda.forms import EventCalendarForm
            context['event_calendar_form'] = EventCalendarForm()
        except Exception:
            pass

        context['hal_url'] = settings.HAL_URL
        return context

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object():
            page = CustomPage.objects.first()
            if page:
                return redirect(reverse_lazy('page', kwargs={'slug': page.slug}))
            else:
                return super(HomeView, self).dispatch(request, *args, **kwargs)
        else:
            return super(HomeView, self).dispatch(request, *args, **kwargs)


class DynamicContentHomeSliderView(Select2QuerySetSequenceView):

    paginate_by = settings.DAL_MAX_RESULTS

    def get_queryset(self):

        articles = Article.objects.all()
        custompage = CustomPage.objects.all()
        events = Event.objects.all()
        persons = Person.objects.all()
        medias = Media.objects.all()

        if self.q:
            articles = articles.filter(title__icontains=self.q)\
                .order_by("-publish_date")
            custompage = custompage.filter(title__icontains=self.q)\
                .order_by("-publish_date")
            events = events.filter(title__icontains=self.q).order_by("-start")
            persons = persons.filter(title__icontains=self.q)
            medias = medias.filter(title__icontains=self.q).order_by("-publish_date")

        qs = autocomplete.QuerySetSequence(
            articles,
            custompage,
            events,
            persons,
            medias
        )
        # Unlimited queryset
        # https://django-autocomplete-light.readthedocs.io/en/master/_modules/dal_queryset_sequence/views.html
        # qs = self.mixup_querysets(qs)
        querysets = list(qs.get_querysets())
        qs = QuerySetSequence(*[q for q in querysets])

        return qs

    def get_results(self, context):
        results = autocomplete_result_formatting(self, context)
        return results


class DynamicContentHomeBodyView(Select2QuerySetSequenceView):

    paginate_by = settings.DAL_MAX_RESULTS

    def get_queryset(self):

        articles = Article.objects.all()
        custompage = CustomPage.objects.all()
        events = Event.objects.all()
        briefs = Brief.objects.all()
        medias = Media.objects.all()
        persons = Person.objects.all()
        projects = Project.objects.all()
        playlists = Playlist.objects.all()

        if self.q:
            articles = articles.filter(title__icontains=self.q)\
                .order_by("-publish_date")
            custompage = custompage.filter(title__icontains=self.q)\
                .order_by("-publish_date")
            events = events.filter(title__icontains=self.q).order_by("-start")
            briefs = briefs.filter(title__icontains=self.q)
            medias = medias.filter(title__icontains=self.q)
            persons = persons.filter(title__icontains=self.q)
            projects = projects.filter(title__icontains=self.q)
            playlists = playlists.filter(title__icontains=self.q)

        qs = autocomplete.QuerySetSequence(
            articles,
            custompage,
            briefs,
            events,
            medias,
            persons,
            projects,
            playlists
        )

        querysets = list(qs.get_querysets())
        qs = QuerySetSequence(*[q for q in querysets])

        return qs

    def get_results(self, context):
        results = autocomplete_result_formatting(self, context)
        return results


class DynamicContentHomeMediaView(Select2QuerySetSequenceView):

    paginate_by = settings.DAL_MAX_RESULTS

    def get_queryset(self):

        playlists = Playlist.objects.all()

        if self.q:
            playlists = playlists.filter(title__icontains=self.q)

        qs = autocomplete.QuerySetSequence(playlists,)

        if self.q:
            qs = qs.filter(title__icontains=self.q)

        querysets = list(qs.get_querysets())
        qs = QuerySetSequence(*[q for q in querysets])

        return qs


class NewsletterView(TemplateView):

    template_name = "pages/newsletter.html"


class PublicationsView(FormView):

    template_name = "pages/publications.html"
    form_class = YearForm
    success_url = "."
    hal_url = settings.HAL_URL
    year = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._hal_url = PublicationsView.hal_url

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        form = self.get_form()
        context = {}
        if form.is_valid():
            context['hal_url'] = self._hal_url +\
                "&annee_publideb=%s&annee_publifin=%s" % (
                    form.cleaned_data['year'],
                    form.cleaned_data['year']
                )
        else:
            context['hal_url'] = self._hal_url
        return render(self.request, 'core/inc/hal.html', context)

    def get_context_data(self, **kwargs):
        context = super(PublicationsView, self).get_context_data(**kwargs)
        context['hal_url'] = self._hal_url
        return context


class InformationView(ListView):

    model = Organization
    context_object_name = 'organizations'
    template_name = "pages/informations.html"

    def get_queryset(self, **kwargs):
        return self.model.objects.filter(is_on_map=True)

    def get_context_data(self, **kwargs):
        context = super(InformationView, self).get_context_data(**kwargs)
        context['organization_types'] = self.get_queryset().values_list(
            'type__name',
            'type__css_class'
        ).order_by('type__name').distinct('type__name')
        return context


class DynamicContentPageView(Select2QuerySetSequenceView):

    paginate_by = settings.DAL_MAX_RESULTS

    def get_queryset(self):

        articles = Article.objects.all()
        custompage = CustomPage.objects.all()
        events = Event.objects.all()
        extended_custompage = ExtendedCustomPage.objects.all()
        projects = ProjectPage.objects.all()
        products = Product.objects.all()

        if self.q:
            articles = articles.filter(title__icontains=self.q)
            custompage = custompage.filter(title__icontains=self.q)
            extended_custompage = extended_custompage.filter(title__icontains=self.q)
            events = events.filter(title__icontains=self.q)
            projects = projects.filter(title__icontains=self.q)
            products = products.filter(title__icontains=self.q)

        qs = autocomplete.QuerySetSequence(
            articles,
            custompage,
            extended_custompage,
            events,
            projects,
            products
        )

        if self.q:
            qs = qs.filter(title__icontains=self.q)

        qs = self.mixup_querysets(qs)

        return qs

    def get_results(self, context):
        results = autocomplete_result_formatting(self, context)
        return results
