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

from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from dal import autocomplete
from dal_select2_queryset_sequence.views import Select2QuerySetSequenceView
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _
from mezzanine.conf import settings
from organization.pages.models import CustomPage, ExtendedCustomPage
from organization.core.views import SlugMixin, autocomplete_result_formatting
from organization.magazine.models import Article, Topic, Brief
from organization.pages.models import Home
from organization.agenda.models import Event
from organization.media.models import Playlist, Media
from organization.network.models import Person, Organization
from organization.projects.models import Project, ProjectResidency
from django.shortcuts import redirect
from django.contrib.contenttypes.models import ContentType
import random


class HomeView(SlugMixin, DetailView):

    model = Home
    template_name = 'index.html'
    context_object_name = 'home'
    body_model_list = ['person', 'article', 'project', 'event', 'projectresidency', 'organization']

    def get_object(self, **kwargs):
        homes = self.model.objects.published()
        if homes:
            return homes.latest("publish_date")
        return None

    def get_body(self, model_type):
        if self.request.user.is_authenticated():
            ct = ContentType.objects.filter(model=model_type)[0]
            model = ct.model_class()
            if model_type == 'person':
                residencies = ProjectResidency.objects.filter(validated=True)
                objects = [residency.artist for residency in residencies]
            else:
                objects = list(model.objects.all())
            return random.sample(objects, k=1)[0]
        else:
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
        except:
            pass

        self.bodys = self.object.dynamiccontenthomebody_set.all()
        for body_model in self.body_model_list:
            context[body_model] = self.get_body(body_model)
            # print(context)
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
        persons = Person.objects.published()
        medias = Media.objects.all()

        if self.q:
            articles = articles.filter(title__icontains=self.q)
            custompage = custompage.filter(title__icontains=self.q)
            events = events.filter(title__icontains=self.q)
            persons = persons.filter(title__icontains=self.q)
            medias = medias.filter(title__icontains=self.q)

        qs = autocomplete.QuerySetSequence(articles, custompage, events, persons, medias)

        if self.q:
            # This would apply the filter on all the querysets
            qs = qs.filter(title__icontains=self.q)

        # This will limit each queryset so that they show an equal number
        # of results.
        qs = self.mixup_querysets(qs)

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

        if self.q:
            articles = articles.filter(title__icontains=self.q)
            custompage = custompage.filter(title__icontains=self.q)
            events = events.filter(title__icontains=self.q)
            briefs = briefs.filter(title__icontains=self.q)
            medias = medias.filter(title__icontains=self.q)
            persons = persons.filter(title__icontains=self.q)
            projects = projects.filter(title__icontains=self.q)

        qs = autocomplete.QuerySetSequence(articles, custompage, briefs, events, medias, persons, projects)

        if self.q:
            # This would apply the filter on all the querysets
            qs = qs.filter(title__icontains=self.q)

        # This will limit each queryset so that they show an equal number
        # of results.
        qs = self.mixup_querysets(qs)

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

        qs = self.mixup_querysets(qs)
        return qs


class NewsletterView(TemplateView):

    template_name = "pages/newsletter.html"


class InformationView(ListView):

    model = Organization
    context_object_name = 'organizations'
    template_name = "pages/informations.html"

    def get_queryset(self, **kwargs):
        return self.model.objects.filter(is_on_map=True)

    def get_context_data(self, **kwargs):
        context = super(InformationView, self).get_context_data(**kwargs)
        context['organization_types'] = self.get_queryset().values_list('type__name', 'type__css_class').order_by('type__name').distinct('type__name')
        return context


class DynamicContentPageView(Select2QuerySetSequenceView):

    paginate_by = settings.DAL_MAX_RESULTS

    def get_queryset(self):

        articles = Article.objects.all()
        custompage = CustomPage.objects.all()
        events = Event.objects.all()
        extended_custompage = ExtendedCustomPage.objects.all()

        if self.q:
            articles = articles.filter(title__icontains=self.q)
            custompage = custompage.filter(title__icontains=self.q)
            extended_custompage = extended_custompage.filter(title__icontains=self.q)
            events = events.filter(title__icontains=self.q)

        qs = autocomplete.QuerySetSequence(articles, custompage, extended_custompage, events)

        if self.q:
            qs = qs.filter(title__icontains=self.q)

        qs = self.mixup_querysets(qs)

        return qs

    def get_results(self, context):
        results = autocomplete_result_formatting(self, context)
        return results
